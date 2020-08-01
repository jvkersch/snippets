export function rotateCube(time: number, cube) {
    time *= 0.001;

    cube.rotation.x = time;
    cube.rotation.y = time;
}

export function rotateCubes(time: number, cubes) {
    time *= 0.001;

    cubes.forEach((cube, ndx) => {
        const speed = 1 + ndx * .1;
        const rot = time * speed;
        cube.rotation.x = rot;
        cube.rotation.y = rot;
    });
}
