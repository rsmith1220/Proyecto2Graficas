import numpy as np
from pyrsistent import m
import matesRS
import array


DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

def reflectVector(normal, direction):
    reflect = 2 * matesRS.dot(normal, direction)
    reflect = np.multiply(reflect, normal)
    reflect = matesRS.subtract(reflect, direction)
    reflect = matesRS.normal2(reflect)
    return reflect

def refractVector(normal, direction, ior):
    # Snell's Law
    cosi = max(-1, min(1, matesRS.dot(direction, normal)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        normal = array(normal) * -1

    eta = etai / etat
    k = 1 - (eta**2) * (1 - (cosi**2) )

    if k < 0: # Total Internal Reflection
        return None

    R = eta * array(direction) + (eta * cosi - k**0.5) * normal
    return R


def fresnel(normal, direction, ior):
    # Fresnel Equation
    cosi = max(-1, min(1, matesRS.dot(direction, normal)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi**2) ** 0.5)


    if sint >= 1: # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint**2) ** 0.5
    cosi = abs(cosi)

    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))

    return (Rs**2 + Rp**2) / 2


class DirectionalLight(object):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = matesRS.normal2(direction)
        self.intensity = intensity
        self.color = color
        self.lightType = DIR_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = array(self.direction) * -1
        intensity = matesRS.dot(intersect.normal, light_dir) * self.intensity
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = array([intensity * self.color[0],
                                 intensity * self.color[1],
                                 intensity * self.color[2]])

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = array(self.direction) * -1
        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = matesRS.subtract( raytracer.camPosition, intersect.point)
        view_dir = matesRS.normal2(view_dir)

        spec_intensity = self.intensity * max(0,matesRS.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = array([spec_intensity * self.color[0],
                              spec_intensity * self.color[1],
                              spec_intensity * self.color[2]])

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = array(self.direction) * -1

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class PointLight(object):
    def __init__(self, point, constant = 1.0, linear = 0.1, quad = 0.05, color = (1,1,1)):
        self.point = point
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = matesRS.subtract(self.point, intersect.point)
        light_dir = matesRS.normal2(light_dir)

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
        #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0
        intensity = matesRS.dot(intersect.normal, light_dir) * attenuation
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = np.array([intensity * self.color[0],
                                 intensity * self.color[1],
                                 intensity * self.color[2]])

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = matesRS.subtract(self.point, intersect.point)
        light_dir = matesRS.normal2(light_dir)

        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = matesRS.subtract( raytracer.camPosition, intersect.point)
        view_dir = matesRS.normal2(view_dir)

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
        #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0

        spec_intensity = attenuation * max(0,matesRS.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = np.array([spec_intensity * self.color[0],
                              spec_intensity * self.color[1],
                              spec_intensity * self.color[2]])

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = matesRS.subtract(self.point, intersect.point)
        light_distance = np.linalg.norm(light_dir)
        light_dir = light_dir / light_distance

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            if shadow_intersect.distance < light_distance:
                shadow_intensity = 1

        return shadow_intensity


class AmbientLight(object):
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        return np.array(self.color) * self.intensity

    def getSpecColor(self, intersect, raytracer):
        return np.array([0,0,0])

    def getShadowIntensity(self, intersect, raytracer):
        return 0