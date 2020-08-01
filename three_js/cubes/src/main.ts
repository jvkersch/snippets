import {
    createRenderer, createPerspectiveCamera,
    createTexturedInstance, createScene, createLighting,
    createCubeGeometry,
} from "./cubes.js";

import {
    rotateCubes
} from './animation.js';

const canvas = document.querySelector("#c");

const renderer = createRenderer(canvas);
const camera = createPerspectiveCamera();

const geometry = createCubeGeometry();

const scene = createScene();
const light = createLighting();

const cubes = [
    createTexturedInstance(geometry, 0x44aa88, 0),
    createTexturedInstance(geometry, 0x8844aa, -2),
    createTexturedInstance(geometry, 0xaa8844, 2),
];

scene.add(light);
cubes.forEach((cube) => scene.add(cube));

const renderFunction = (time) => {
    rotateCubes(time, cubes);

    renderer.render(scene, camera);
    requestAnimationFrame(renderFunction);
}
requestAnimationFrame(renderFunction);
