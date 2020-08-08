const vertices = [
    [1, 1, 1, 1],    // 0
    [-1, 1, 1, 1],   // 1
    [-1, -1, 1, 1],  // 2
    [1, -1, 1, 1],   // 3
    [1, 1, -1, 1],   // 4
    [-1, 1, -1, 1],  // 5
    [-1, -1, -1, 1], // 6
    [1, -1, -1, 1],  // 7
    [1, 1, 1, -1],   // 8
    [-1, 1, 1, -1],  // 9
    [-1, -1, 1, -1], // 10
    [1, -1, 1, -1],  // 11
    [1, 1, -1, -1],  // 12
    [-1, 1, -1, -1], // 13
    [-1, -1, -1, -1],// 14
    [1, -1, -1, -1], // 15
];
const edges = [
    // top cube
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
    // bottom cube
    [8, 9],
    [9, 10],
    [10, 11],
    [11, 8],
    [12, 13],
    [13, 14],
    [14, 15],
    [15, 12],
    [8, 12],
    [9, 13],
    [10, 14],
    [11, 15],
    // connecting edges
    [0, 8],
    [1, 9],
    [2, 10],
    [3, 11],
    [4, 12],
    [5, 13],
    [6, 14],
    [7, 15]
];


class LineCubeModel {
    // A special kind of LineSegments

    constructor() {
        const geometry = new THREE.Geometry();
        for (const e of edges) {
            const src = to3d(vertices[e[0]]), tgt = to3d(vertices[e[1]]);
            geometry.vertices.push(new THREE.Vector3(...src));
            geometry.vertices.push(new THREE.Vector3(...tgt));
        }

        const material = new THREE.LineBasicMaterial({
            color: 0x000000,
            linewidth: 1,
        });

        this.object = new THREE.LineSegments(geometry, material);
    }

    rotate(theta1, theta2) {
        const c1 = Math.cos(theta1), s1 = Math.sin(theta1);
        const c2 = Math.cos(theta2), s2 = Math.sin(theta2);
        const geometry = this.object.geometry;

        let i = 0;
        for (const e of edges) {
            const src = vertices[e[0]], tgt = vertices[e[1]];
            const srcTf = to3d(rotate(src, c1, s1, c2, s2));
            const tgtTf = to3d(rotate(tgt, c1, s1, c2, s2));

            geometry.vertices[i++].set(...srcTf);
            geometry.vertices[i++].set(...tgtTf);
        }
        geometry.verticesNeedUpdate = true;
    }

}


export class CubeRenderer {
    constructor(omega1, omega2) {
        this.omega1 = omega1;
        this.omega2 = omega2;

        this.cubeModel = new LineCubeModel();
    }

    setupScene() {

        const canvas = document.querySelector('#c');
        const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });

        const camera = createCamera();
        const scene = createScene();

        const _ = new THREE.OrbitControls(camera, renderer.domElement);

        this._renderFun = () => renderer.render(scene, camera);
        this._scene = scene;
        this.camera = camera;
        this.renderer = renderer;

        scene.add(this.cubeModel.object);
    }

    animate() {
        const render = (time) => {
            time *= 0.001;

            const theta1 = 2.0 * Math.PI * this.omega1 * time;
            const theta2 = 2.0 * Math.PI * this.omega2 * time;

            this.cubeModel.rotate(theta1, theta2);

            this._renderFun();
            requestAnimationFrame(render);
        };
        requestAnimationFrame(render);
    }
}


function to3d(vertex4d, h = 3) {
    // Stereographic projection of a four-dimensional point with coordinates
    // (x, y, z, u) onto the u = 0 plane. The vantage point for the projection
    // is at (0, 0, 0, h). The default h = 3 is chosen so that the "inner"
    // cube (corresponding to u = -1 in 4D) is twice as small as the "outer"
    // cube (u = +1).

    const [x, y, z, u] = vertex4d;
    const f = h / (h - u);
    return [f * x, f * y, f * z];
}

function rotate(vertex4d, c1, s1, c2, s2) {
    // Apply a double rotation to a vertex. The (x, y) coordinates are
    // rotated over an angle theta1, and the (z, u) coordinates over an
    // angle theta2. Only the cosine and the sine of theta1,2 are passed
    // in, to avoid having to recompute them.

    const [x, y, z, u] = vertex4d;
    return [
        c1 * x - s1 * y,
        s1 * x + c1 * y,
        c2 * z + s2 * u,
        -s2 * z + c2 * u
    ];
}

function createScene() {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    return scene;
}

function createCamera() {
    const fov = 40;
    const aspect = 2;  // the canvas default
    const near = 0.1;
    const far = 1000;
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

    camera.position.set(5, 5 - 1.5, 5 + 2.0);
    camera.lookAt(0, 0, 0);

    return camera;
}
