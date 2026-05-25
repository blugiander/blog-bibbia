// Matrix Rain Effect
document.addEventListener("DOMContentLoaded", () => {
    // Inject Canvas for Background
    const canvas = document.createElement("canvas");
    canvas.id = "matrix-bg";
    document.body.prepend(canvas);

    const ctx = canvas.getContext("2d");
    
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    const str = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const matrix = str.split("");

    const font_size = 14;
    let columns = width / font_size;
    let drops = [];

    for (let x = 0; x < columns; x++) {
        drops[x] = 1;
    }

    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, width, height);

        ctx.fillStyle = "#00ff00"; // Green text
        ctx.font = font_size + "px 'Fira Code', monospace";

        for (let i = 0; i < drops.length; i++) {
            const text = matrix[Math.floor(Math.random() * matrix.length)];
            ctx.fillText(text, i * font_size, drops[i] * font_size);

            if (drops[i] * font_size > height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(draw, 35);

    window.addEventListener("resize", () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        columns = width / font_size;
        drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = 1;
        }
    });

    // Animate Header Containers
    const headers = document.querySelectorAll('.matrix-header-container');
    headers.forEach(h => {
        const hc = document.createElement('canvas');
        hc.width = h.clientWidth;
        hc.height = h.clientHeight;
        hc.style.position = 'absolute';
        hc.style.top = '0';
        hc.style.left = '0';
        hc.style.zIndex = '1';
        h.appendChild(hc);
        
        const hctx = hc.getContext('2d');
        const hCols = hc.width / 10;
        const hDrops = Array(Math.floor(hCols)).fill(1);
        
        setInterval(() => {
            hctx.fillStyle = "rgba(0, 0, 0, 0.1)";
            hctx.fillRect(0, 0, hc.width, hc.height);
            hctx.fillStyle = "#00ff00";
            hctx.font = "10px monospace";
            for (let i = 0; i < hDrops.length; i++) {
                const text = Math.random() > 0.5 ? "1" : "0";
                hctx.fillText(text, i * 10, hDrops[i] * 10);
                if (hDrops[i] * 10 > hc.height && Math.random() > 0.9) hDrops[i] = 0;
                hDrops[i]++;
            }
        }, 50);
    });
});
