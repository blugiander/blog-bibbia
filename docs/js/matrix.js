// Matrix Rain Effect
document.addEventListener("DOMContentLoaded", () => {
    // Inject Canvas for Background
    const canvas = document.createElement("canvas");
    canvas.id = "matrix-bg";
    document.body.prepend(canvas);

    const ctx = canvas.getContext("2d");

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    const chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".split("");
    const FONT_SIZE = 14;

    function makeDrops(w) {
        const count = Math.floor(w / FONT_SIZE);
        return new Int32Array(count).fill(1);
    }

    let drops = makeDrops(width);

    function randomChar() {
        const idx = Math.floor(Math.random() * chars.length);
        return chars.at(idx) ?? "0";
    }

    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, width, height);
        ctx.fillStyle = "#00ff00";
        ctx.font = FONT_SIZE + "px 'Fira Code', monospace";

        drops.forEach((dropY, col) => {
            ctx.fillText(randomChar(), col * FONT_SIZE, dropY * FONT_SIZE);
            const shouldReset = dropY * FONT_SIZE > height && Math.random() > 0.975;
            drops[col] = shouldReset ? 0 : dropY + 1;
        });
    }

    setInterval(draw, 35);

    window.addEventListener("resize", () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        drops = makeDrops(width);
    });

    // Animate Header Containers
    const HEADER_FONT = 10;

    document.querySelectorAll(".matrix-header-container").forEach(h => {
        const hc = document.createElement("canvas");
        hc.width = h.clientWidth;
        hc.height = h.clientHeight;
        Object.assign(hc.style, { position: "absolute", top: "0", left: "0", zIndex: "1" });
        h.appendChild(hc);

        const hctx = hc.getContext("2d");
        const hDrops = new Int32Array(Math.floor(hc.width / HEADER_FONT)).fill(1);

        setInterval(() => {
            hctx.fillStyle = "rgba(0, 0, 0, 0.1)";
            hctx.fillRect(0, 0, hc.width, hc.height);
            hctx.fillStyle = "#00ff00";
            hctx.font = HEADER_FONT + "px monospace";

            hDrops.forEach((dropY, col) => {
                const bit = Math.random() > 0.5 ? "1" : "0";
                hctx.fillText(bit, col * HEADER_FONT, dropY * HEADER_FONT);
                const shouldReset = dropY * HEADER_FONT > hc.height && Math.random() > 0.9;
                hDrops[col] = shouldReset ? 0 : dropY + 1;
            });
        }, 50);
    });
});
