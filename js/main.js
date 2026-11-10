const root = document.documentElement;
const themeToggle = document.querySelector("#theme-toggle");
const menuToggle = document.querySelector("#menu-toggle");
const navLinks = document.querySelector("#nav-links");
const year = document.querySelector("#current-year");
const progressBar = document.querySelector("#scroll-progress");
const themeColor = document.querySelector('meta[name="theme-color"]');
const sectionLinks = [...(navLinks?.querySelectorAll('a[href^="#"]') || [])];
const firstSection = sectionLinks[0]
  ? document.querySelector(sectionLinks[0].getAttribute("href"))
  : null;

// Theme preference is stored only in the visitor's browser.
let savedTheme = null;
try {
  savedTheme = localStorage.getItem("portfolio-theme");
} catch {
  // The page remains usable when browser storage is unavailable.
}
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const initialTheme = ["light", "dark"].includes(savedTheme)
  ? savedTheme
  : prefersDark ? "dark" : "light";

function applyTheme(theme) {
  root.dataset.theme = theme;
  const isDark = theme === "dark";
  themeColor?.setAttribute("content", isDark ? "#070b13" : "#f5f7fb");
  themeToggle?.setAttribute("aria-pressed", String(isDark));
  themeToggle?.setAttribute(
    "aria-label",
    isDark ? "Switch to light mode" : "Switch to dark mode",
  );
}

applyTheme(initialTheme);

themeToggle?.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(nextTheme);
  try {
    localStorage.setItem("portfolio-theme", nextTheme);
  } catch {
    // Theme switching still works for this visit without persistence.
  }
});

function closeMenu() {
  navLinks?.classList.remove("is-open");
  document.body.classList.remove("menu-open");
  menuToggle?.setAttribute("aria-expanded", "false");
  menuToggle?.setAttribute("aria-label", "Open navigation");
}

menuToggle?.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  navLinks?.classList.toggle("is-open", !isOpen);
  document.body.classList.toggle("menu-open", !isOpen);
  menuToggle.setAttribute("aria-expanded", String(!isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Open navigation" : "Close navigation");
});

navLinks?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", closeMenu);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeMenu();
});

window.addEventListener("resize", () => {
  if (window.innerWidth >= 900) closeMenu();
});

function updateScrollProgress() {
  if (!progressBar) return;
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollable > 0 ? Math.min(window.scrollY / scrollable, 1) : 0;
  progressBar.style.transform = `scaleX(${progress})`;

  const beforeFirstSection = firstSection
    ? window.scrollY < firstSection.offsetTop - window.innerHeight * 0.45
    : false;

  if (beforeFirstSection) {
    sectionLinks.forEach((link) => link.removeAttribute("aria-current"));
  }
}

window.addEventListener("scroll", updateScrollProgress, { passive: true });
window.addEventListener("resize", updateScrollProgress);
updateScrollProgress();

const observedSections = sectionLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

if ("IntersectionObserver" in window && observedSections.length) {
  const navigationObserver = new IntersectionObserver(
    (entries) => {
      const visibleSection = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (!visibleSection) return;

      sectionLinks.forEach((link) => {
        const isCurrent = link.getAttribute("href") === `#${visibleSection.target.id}`;
        if (isCurrent) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
      });
    },
    { rootMargin: "-28% 0px -58%", threshold: [0, 0.2, 0.5] },
  );

  observedSections.forEach((section) => navigationObserver.observe(section));
}

if (year) year.textContent = String(new Date().getFullYear());

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealElements = document.querySelectorAll(".reveal");

if (reducedMotion || !("IntersectionObserver" in window)) {
  revealElements.forEach((element) => element.classList.add("is-visible"));
} else {
  root.classList.add("has-reveal");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.12 },
  );

  revealElements.forEach((element, index) => {
    element.style.transitionDelay = `${Math.min(index % 4, 3) * 55}ms`;
    observer.observe(element);
  });
}

/* ================= Visual effects ================= */
const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

// Typewriter that cycles through what I build.
const typer = document.querySelector("#typer");
if (typer && !reducedMotion) {
  const words = (typer.dataset.words || "").split("|").filter(Boolean);
  let wordIndex = 0;
  let charIndex = 0;
  let deleting = false;
  typer.textContent = "";
  typer.classList.add("is-typing");

  const tick = () => {
    const word = words[wordIndex];
    charIndex += deleting ? -1 : 1;
    typer.textContent = word.slice(0, charIndex);

    let delay = deleting ? 38 : 70 + Math.random() * 50;
    if (!deleting && charIndex === word.length) {
      delay = 1900;
      deleting = true;
    } else if (deleting && charIndex === 0) {
      deleting = false;
      wordIndex = (wordIndex + 1) % words.length;
      delay = 380;
    }
    setTimeout(tick, delay);
  };
  setTimeout(tick, 600);
} else if (typer) {
  typer.textContent = "web applications, APIs, and data-driven systems.";
}

// Hero particle network that reacts to the pointer.
const canvas = document.querySelector("#hero-canvas");
const hero = document.querySelector(".hero");
if (canvas && hero && !reducedMotion) {
  const ctx = canvas.getContext("2d");
  const pointer = { x: -9999, y: -9999 };
  let particles = [];
  let width = 0;
  let height = 0;
  let running = true;
  let rgb = "50, 102, 232";

  const readColor = () => {
    rgb = root.dataset.theme === "dark" ? "127, 165, 255" : "50, 102, 232";
  };

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = hero.offsetWidth;
    height = hero.offsetHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.round(Math.min(90, (width * height) / 14000));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.6 + 0.6,
    }));
  };

  const draw = () => {
    if (!running) return;
    ctx.clearRect(0, 0, width, height);
    const linkDist = 130;

    for (const p of particles) {
      const dx = p.x - pointer.x;
      const dy = p.y - pointer.y;
      const dist = Math.hypot(dx, dy);
      if (dist < 140 && dist > 0) {
        const force = (140 - dist) / 140;
        p.vx += (dx / dist) * force * 0.25;
        p.vy += (dy / dist) * force * 0.25;
      }
      p.vx *= 0.97;
      p.vy *= 0.97;
      p.vx += (Math.random() - 0.5) * 0.02;
      p.vy += (Math.random() - 0.5) * 0.02;
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;
      p.x = Math.max(0, Math.min(width, p.x));
      p.y = Math.max(0, Math.min(height, p.y));
    }

    for (let i = 0; i < particles.length; i += 1) {
      const a = particles[i];
      for (let j = i + 1; j < particles.length; j += 1) {
        const b = particles[j];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < linkDist) {
          ctx.strokeStyle = `rgba(${rgb}, ${(1 - d / linkDist) * 0.32})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
      const near = Math.hypot(a.x - pointer.x, a.y - pointer.y) < 180;
      ctx.fillStyle = `rgba(${rgb}, ${near ? 0.95 : 0.6})`;
      ctx.beginPath();
      ctx.arc(a.x, a.y, near ? a.r + 0.8 : a.r, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(draw);
  };

  hero.addEventListener("pointermove", (event) => {
    const rect = hero.getBoundingClientRect();
    pointer.x = event.clientX - rect.left;
    pointer.y = event.clientY - rect.top;
  });
  hero.addEventListener("pointerleave", () => {
    pointer.x = -9999;
    pointer.y = -9999;
  });

  // Pause the animation when the hero is off-screen or the tab is hidden.
  new IntersectionObserver(([entry]) => {
    const wasRunning = running;
    running = entry.isIntersecting && !document.hidden;
    if (running && !wasRunning) requestAnimationFrame(draw);
  }).observe(hero);
  document.addEventListener("visibilitychange", () => {
    const wasRunning = running;
    running = !document.hidden;
    if (running && !wasRunning) requestAnimationFrame(draw);
  });

  new MutationObserver(readColor).observe(root, { attributes: true, attributeFilter: ["data-theme"] });
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 150);
  });

  readColor();
  resize();
  requestAnimationFrame(draw);
}

// Count numbers up when they scroll into view.
const counters = document.querySelectorAll(".count[data-count]");
if (counters.length && !reducedMotion && "IntersectionObserver" in window) {
  const countObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = Number(el.dataset.count);
        const start = performance.now();
        const duration = 1100;
        const step = (now) => {
          const t = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - t, 3);
          el.textContent = String(Math.round(target * eased));
          if (t < 1) requestAnimationFrame(step);
        };
        el.textContent = "0";
        requestAnimationFrame(step);
        countObserver.unobserve(el);
      });
    },
    { threshold: 0.8 },
  );
  counters.forEach((el) => countObserver.observe(el));
}

if (finePointer && !reducedMotion) {
  // 3D tilt with a moving glare on the profile card.
  document.querySelectorAll("[data-tilt]").forEach((card) => {
    const glare = card.querySelector(".tilt-glare");
    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      const px = (event.clientX - rect.left) / rect.width;
      const py = (event.clientY - rect.top) / rect.height;
      card.classList.add("is-tilting");
      card.style.transform = `perspective(900px) rotateX(${(0.5 - py) * 12}deg) rotateY(${(px - 0.5) * 14}deg) scale(1.02)`;
      glare?.style.setProperty("--gx", `${px * 100}%`);
      glare?.style.setProperty("--gy", `${py * 100}%`);
    });
    card.addEventListener("pointerleave", () => {
      card.classList.remove("is-tilting");
      card.style.transform = "";
    });
  });

  // Spotlight border that follows the cursor across cards.
  const glowCards = document.querySelectorAll(
    ".project-card, .skill-card, .more-card, .activity-card, .education-panel",
  );
  glowCards.forEach((card) => {
    card.classList.add("glow");
    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty("--mx", `${event.clientX - rect.left}px`);
      card.style.setProperty("--my", `${event.clientY - rect.top}px`);
    });
  });

  // Buttons that lean toward the cursor.
  document.querySelectorAll("[data-magnetic]").forEach((button) => {
    button.addEventListener("pointermove", (event) => {
      const rect = button.getBoundingClientRect();
      const x = event.clientX - rect.left - rect.width / 2;
      const y = event.clientY - rect.top - rect.height / 2;
      button.classList.add("is-magnet");
      button.style.transform = `translate(${x * 0.25}px, ${y * 0.35}px)`;
    });
    button.addEventListener("pointerleave", () => {
      button.classList.remove("is-magnet");
      button.style.transform = "";
    });
  });
}
