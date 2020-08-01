import * as THREE from '../node_modules/three/build/three.module.js';
//import * as THREE from 'three';

export function createRenderer(canvas) {
    const renderer = new THREE.WebGLRenderer({ canvas });
    return renderer;
}

export function createPerspectiveCamera(): THREE.Camera {
    const fov = 75;
    const aspect = 2;
    const near = 0.1;
    const far = 5;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

    camera.position.z = 2;
    return camera;
}

export function createScene(): THREE.Scene {
    return new THREE.Scene();
}

export function createCubeGeometry(): THREE.Geometry {
    const boxWidth = 1;
    const boxHeight = 1;
    const boxDepth = 1;
    return new THREE.BoxGeometry(boxWidth, boxHeight, boxDepth);
}

export function createTexturedInstance(geometry, color, x = 0, y = 0, z = 0): THREE.Mesh {
    const material = new THREE.MeshPhongMaterial({ color: color });
    const instance = new THREE.Mesh(geometry, material);
    instance.position.x = x;
    instance.position.y = y;
    instance.position.z = z;

    return instance;
}

export function createLighting(): THREE.Light {
    const color = 0xffffff;
    const intensity = 1;
    const light = new THREE.DirectionalLight(color, intensity);
    light.position.set(-1, 2, 4);
    return light;
}
