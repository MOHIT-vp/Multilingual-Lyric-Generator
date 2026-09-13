"""JavaScript animations and interactions for the KPR (Keepers) website."""


def get_js() -> str:
    return '''
(function () {
  "use strict";

  /* =======================================================================
     UTILITIES
     ======================================================================= */
  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }
  function qsa(sel, ctx) { return Array.from((ctx || document).querySelectorAll(sel)); }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function rand(lo, hi) { return Math.random() * (hi - lo) + lo; }

  /* =======================================================================
     1.  PRELOADER SYSTEM
     ======================================================================= */
  function initPreloader() {
    var preloader    = qs('.preloader');
    var progressBar  = qs('.preloader-progress-bar');
    var progressText = qs('.preloader-percent');

    if (!preloader) { onPreloaderDone(); return; }

    var progress = { value: 0 };

    gsap.to(progress, {
      value: 100,
      duration: 2.5,
      ease: 'power2.inOut',
      onUpdate: function () {
        var v = Math.round(progress.value);
        if (progressBar)  progressBar.style.transform = 'scaleX(' + (v / 100) + ')';
        if (progressText) progressText.textContent = v + '%';
      },
      onComplete: function () {
        gsap.to(preloader, {
          opacity: 0,
          duration: 0.6,
          ease: 'power2.inOut',
          onComplete: function () {
            preloader.style.display = 'none';
            onPreloaderDone();
          }
        });
      }
    });
  }

  function onPreloaderDone() {
    initThreeJS();
    initFrame();
    initScrollAnimations();
    initMenu();
    initConsole();
    initAudioButton();
    initTableaux();
    initGallery();
    initCounter();
    initLandingAnimations();
  }

  /* =======================================================================
     2.  GSAP + SCROLLTRIGGER SETUP
     ======================================================================= */
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  /* =======================================================================
     3.  FRAME SYSTEM
     ======================================================================= */
  function initFrame() {
    var lightFrame   = qs('.the-frame--light');
    var darkFrame    = qs('.the-frame--dark');
    var progressFill = qs('.frame-progress-fill');
    var subLinks     = qsa('.submenu-link');
    var sections     = qsa('.section');

    if (!sections.length) return;

    function updateFrame(sectionEl) {
      if (!sectionEl) return;
      var isDark = sectionEl.classList.contains('section--dark') ||
                   sectionEl.classList.contains('section--black');

      if (lightFrame && darkFrame) {
        if (isDark) {
          lightFrame.classList.remove('is-visible');
          darkFrame.classList.add('is-visible');
        } else {
          darkFrame.classList.remove('is-visible');
          lightFrame.classList.add('is-visible');
        }
      }

      var id = sectionEl.getAttribute('id') || '';
      subLinks.forEach(function (link) {
        var href = (link.getAttribute('href') || '').replace('#', '');
        link.classList.toggle('is-active', href === id);
      });
    }

    sections.forEach(function (sec, i) {
      ScrollTrigger.create({
        trigger: sec,
        start: 'top center',
        end: 'bottom center',
        onEnter: function () { updateFrame(sec); },
        onEnterBack: function () { updateFrame(sec); },
        onUpdate: function (self) {
          if (progressFill) {
            progressFill.style.transform = 'scaleY(' + self.progress + ')';
          }
        }
      });
    });
  }

  /* =======================================================================
     4.  LANDING SECTION ANIMATIONS
     ======================================================================= */
  function initLandingAnimations() {
    var wordReveals = qsa('.word-reveal');

    wordReveals.forEach(function (container) {
      var children = Array.from(container.children);
      if (!children.length) {
        var text = container.textContent;
        container.innerHTML = '';
        text.split(' ').forEach(function (word) {
          var span = document.createElement('span');
          span.style.display = 'inline-block';
          span.style.overflow = 'hidden';
          var inner = document.createElement('span');
          inner.style.display = 'inline-block';
          inner.textContent = word + '\\u00A0';
          span.appendChild(inner);
          container.appendChild(span);
        });
        children = Array.from(container.querySelectorAll('span > span'));
      }

      gsap.fromTo(children, {
        y: '100%',
        opacity: 0
      }, {
        y: '0%',
        opacity: 1,
        duration: 0.8,
        ease: 'power3.out',
        stagger: 0.15
      });
    });

    var scrollIndicator = qs('.scroll-indicator');
    if (scrollIndicator) {
      gsap.to(scrollIndicator, {
        y: 8,
        opacity: 0.6,
        duration: 1.2,
        ease: 'power1.inOut',
        repeat: -1,
        yoyo: true
      });

      ScrollTrigger.create({
        trigger: 'body',
        start: 'top top',
        end: '200px top',
        onUpdate: function (self) {
          gsap.set(scrollIndicator, { opacity: 1 - self.progress });
        }
      });
    }
  }

  /* =======================================================================
     5.  HACKY TEXT ANIMATION CLASS
     ======================================================================= */
  function HackyText(el) {
    this.el = el;
    this.originalText = el.dataset.text || el.textContent;
    this.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    this.isAnimating = false;
  }

  HackyText.prototype.animate = function (duration) {
    if (this.isAnimating) return;
    this.isAnimating = true;
    duration = duration || 1500;

    var self = this;
    var text = this.originalText;
    var length = text.length;
    var startTime = performance.now();
    var resolvedCount = 0;

    function step(now) {
      var elapsed = now - startTime;
      var progress = clamp(elapsed / duration, 0, 1);
      var targetResolved = Math.floor(progress * length);
      var display = '';

      for (var i = 0; i < length; i++) {
        if (text[i] === ' ') {
          display += ' ';
        } else if (i < targetResolved) {
          display += text[i];
        } else {
          display += self.chars[Math.floor(Math.random() * self.chars.length)];
        }
      }

      self.el.textContent = display;

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        self.el.textContent = text;
        self.isAnimating = false;
      }
    }

    requestAnimationFrame(step);
  };

  /* =======================================================================
     6.  DOT-CAPTION ANIMATION
     ======================================================================= */
  function animateDotCaption(el) {
    if (!el || el.dataset.animated === '1') return;
    el.dataset.animated = '1';

    var dot = el.querySelector('.dot-caption-dot');
    var textEl = el.querySelector('.dot-caption-text');

    if (dot) {
      gsap.fromTo(dot, { opacity: 0, scale: 0 }, {
        opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)'
      });
    }

    if (textEl) {
      var original = textEl.textContent;
      textEl.innerHTML = '';
      original.split('').forEach(function (ch) {
        var span = document.createElement('span');
        span.textContent = ch;
        span.style.opacity = '0';
        span.style.display = 'inline-block';
        if (ch === ' ') span.style.width = '0.25em';
        textEl.appendChild(span);
      });

      gsap.to(textEl.querySelectorAll('span'), {
        opacity: 1,
        duration: 0.05,
        ease: 'none',
        stagger: 0.03,
        delay: 0.35
      });
    }
  }

  /* =======================================================================
     7.  LINE ANIMATIONS
     ======================================================================= */
  function animateLine(el) {
    if (!el || el.dataset.animated === '1') return;
    el.dataset.animated = '1';

    gsap.fromTo(el, {
      opacity: 0,
      scaleX: 0,
      transformOrigin: 'left center'
    }, {
      opacity: 1,
      scaleX: 1,
      duration: 0.8,
      ease: 'power2.out'
    });
  }

  /* =======================================================================
     8.  PARALLAX EFFECTS
     ======================================================================= */
  function initParallax() {
    qsa('.js-parallax').forEach(function (el) {
      var speed = parseFloat(el.dataset.speed) || 0.2;
      var yAmount = 100 * speed;

      gsap.fromTo(el, { y: -yAmount }, {
        y: yAmount,
        ease: 'none',
        scrollTrigger: {
          trigger: el,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true
        }
      });
    });
  }

  /* =======================================================================
     9.  SECTION ENTER ANIMATIONS
     ======================================================================= */
  function initScrollAnimations() {
    initParallax();
    initHackyTexts();

    var sections = qsa('.section');
    sections.forEach(function (sec) {
      var headings = sec.querySelectorAll('h2, .section-title');
      var images   = sec.querySelectorAll('img, .section-image, .gallery-image');
      var captions = sec.querySelectorAll('.dot-caption');
      var lines    = sec.querySelectorAll('.js-line');
      var fadeEls  = sec.querySelectorAll('.js-fade-in');

      var tl = gsap.timeline({
        scrollTrigger: {
          trigger: sec,
          start: 'top 80%',
          end: 'bottom 20%',
          toggleActions: 'play none none none',
          once: true
        }
      });

      headings.forEach(function (h) {
        var words = h.querySelectorAll('.word-reveal > *');
        if (words.length) {
          tl.fromTo(words, {
            y: 74, opacity: 0
          }, {
            y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', stagger: 0.1
          }, 0);
        } else {
          tl.fromTo(h, {
            y: 40, opacity: 0
          }, {
            y: 0, opacity: 1, duration: 0.8, ease: 'power3.out'
          }, 0);
        }
      });

      images.forEach(function (img, i) {
        tl.fromTo(img, {
          opacity: 0, scale: 0.95
        }, {
          opacity: 1, scale: 1, duration: 0.9, ease: 'power2.out'
        }, 0.15 * i);
      });

      captions.forEach(function (cap, i) {
        tl.add(function () { animateDotCaption(cap); }, 0.3 + 0.1 * i);
      });

      lines.forEach(function (line) {
        tl.add(function () { animateLine(line); }, 0.2);
      });

      fadeEls.forEach(function (el, i) {
        tl.fromTo(el, {
          y: 30, opacity: 0
        }, {
          y: 0, opacity: 1, duration: 0.7, ease: 'power2.out'
        }, 0.1 + 0.08 * i);
      });
    });
  }

  /* --- Hacky text scroll triggers --- */
  function initHackyTexts() {
    qsa('.hacky-text').forEach(function (el) {
      var ht = new HackyText(el);
      ScrollTrigger.create({
        trigger: el,
        start: 'top 85%',
        once: true,
        onEnter: function () { ht.animate(1500); }
      });
    });
  }

  /* =======================================================================
     10. COLLECTION COUNTER ANIMATION
     ======================================================================= */
  function initCounter() {
    var counterEl = qs('.counter-value');
    if (!counterEl) return;

    var obj = { val: 0 };
    ScrollTrigger.create({
      trigger: counterEl,
      start: 'top 85%',
      once: true,
      onEnter: function () {
        gsap.to(obj, {
          val: 10,
          duration: 2,
          ease: 'power2.out',
          onUpdate: function () {
            var v = Math.round(obj.val);
            counterEl.textContent = (v < 10 ? '0' : '') + v + 'K';
          }
        });
      }
    });
  }

  /* =======================================================================
     11. COLLECTION GALLERY
     ======================================================================= */
  function initGallery() {
    var gallery = qs('.collection-gallery');
    if (!gallery) return;

    var leftCards  = qsa('.gallery-card--left', gallery);
    var rightCards = qsa('.gallery-card--right', gallery);

    if (!leftCards.length && !rightCards.length) {
      var cards = qsa('.gallery-card', gallery);
      var half = Math.ceil(cards.length / 2);
      leftCards  = cards.slice(0, half);
      rightCards = cards.slice(half);
    }

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: gallery,
        start: 'top 70%',
        end: 'bottom 30%',
        scrub: 1
      }
    });

    leftCards.forEach(function (card, i) {
      tl.fromTo(card, {
        x: 96,
        z: -80 * (i + 1),
        opacity: 0.5
      }, {
        x: 0,
        z: 0,
        opacity: 1,
        duration: 1,
        ease: 'none'
      }, 0);
    });

    rightCards.forEach(function (card, i) {
      tl.fromTo(card, {
        x: -96,
        z: -80 * (i + 1),
        opacity: 0.5
      }, {
        x: 0,
        z: 0,
        opacity: 1,
        duration: 1,
        ease: 'none'
      }, 0);
    });
  }

  /* =======================================================================
     12 + 13.  TABLEAU PINNED SECTIONS + HOLD-TO-EXPLORE
     ======================================================================= */
  function initTableaux() {
    var tableaux = qsa('.tableau-section');
    if (!tableaux.length) return;

    tableaux.forEach(function (tab) {
      var layers   = qsa('.sd-layer', tab);
      var titleEl  = qs('.tableau-title', tab);
      var storyEl  = qs('.tableau-story', tab);
      var btnHold  = qs('.btn-hold', tab);
      var images   = qsa('.sd-layer img, .sd-layer .tableau-image', tab);
      var captions = qsa('.sd-layer .dot-caption', tab);

      /* --- Pinning --- */
      ScrollTrigger.create({
        trigger: tab,
        start: 'top top',
        end: '+=300%',
        pin: true,
        pinSpacing: true
      });

      /* --- Title character animation --- */
      if (titleEl) {
        var titleText = titleEl.textContent;
        titleEl.innerHTML = '';
        titleText.split('').forEach(function (ch) {
          var span = document.createElement('span');
          span.textContent = ch;
          span.style.display = 'inline-block';
          span.style.opacity = '0';
          if (ch === ' ') span.style.width = '0.3em';
          titleEl.appendChild(span);
        });

        ScrollTrigger.create({
          trigger: tab,
          start: 'top 60%',
          once: true,
          onEnter: function () {
            gsap.to(titleEl.querySelectorAll('span'), {
              opacity: 1,
              y: 0,
              duration: 0.06,
              ease: 'none',
              stagger: 0.04
            });
          }
        });
      }

      /* --- Story text fade-in --- */
      if (storyEl) {
        gsap.fromTo(storyEl, { opacity: 0, y: 20 }, {
          opacity: 1, y: 0, duration: 0.8, ease: 'power2.out',
          scrollTrigger: {
            trigger: tab,
            start: 'top 40%',
            toggleActions: 'play none none none',
            once: true
          }
        });
      }

      /* --- Hold-to-explore (layers expand / collapse) --- */
      var origins = [
        '0px 0px',
        '1920px 0px',
        '0px 1080px',
        '1920px 1080px',
        '960px 540px'
      ];

      var expandTL = gsap.timeline({ paused: true });

      layers.forEach(function (layer, i) {
        var ox = origins[i % origins.length];
        layer.style.transformOrigin = ox;

        expandTL.fromTo(layer, {
          scale: 0.6,
          opacity: 0.3
        }, {
          scale: 1,
          opacity: 1,
          duration: 0.8,
          ease: 'power2.out'
        }, i * 0.08);
      });

      images.forEach(function (img, i) {
        expandTL.fromTo(img, { opacity: 0 }, {
          opacity: 1, duration: 0.5, ease: 'power1.out'
        }, 0.3 + i * 0.06);
      });

      captions.forEach(function (cap) {
        expandTL.add(function () { animateDotCaption(cap); }, 0.5);
      });

      if (btnHold) {
        var pressing = false;

        function onDown(e) {
          e.preventDefault();
          pressing = true;
          btnHold.classList.add('is-pressed');
          expandTL.play();
        }

        function onUp() {
          if (!pressing) return;
          pressing = false;
          btnHold.classList.remove('is-pressed');
          expandTL.reverse();
        }

        btnHold.addEventListener('mousedown', onDown);
        btnHold.addEventListener('touchstart', onDown, { passive: false });
        window.addEventListener('mouseup', onUp);
        window.addEventListener('touchend', onUp);
      } else {
        /* auto-expand on scroll if no hold button */
        ScrollTrigger.create({
          trigger: tab,
          start: 'top 30%',
          end: '+=200%',
          scrub: 1,
          onUpdate: function (self) {
            expandTL.progress(self.progress);
          }
        });
      }
    });
  }

  /* =======================================================================
     14. MENU SYSTEM
     ======================================================================= */
  function initMenu() {
    var menuContainer  = qs('.the-menu');
    var hamburgerBtn   = qs('.hamburger-btn');
    var menuCloseBtn   = qs('.menu-close-btn');
    var navItems       = qsa('.menu-nav-item');

    if (!menuContainer) return;

    var menuTL = gsap.timeline({ paused: true });

    menuTL.fromTo(menuContainer, {
      x: '-100%',
      visibility: 'hidden'
    }, {
      x: '0%',
      visibility: 'visible',
      duration: 0.6,
      ease: 'power3.inOut'
    });

    if (navItems.length) {
      menuTL.fromTo(navItems, {
        y: 40,
        opacity: 0
      }, {
        y: 0,
        opacity: 1,
        duration: 0.4,
        ease: 'power2.out',
        stagger: 0.08
      }, '-=0.3');
    }

    function openMenu() {
      document.body.classList.add('menu-open');
      menuTL.play();
    }

    function closeMenu() {
      menuTL.reverse();
      menuTL.eventCallback('onReverseComplete', function () {
        document.body.classList.remove('menu-open');
      });
    }

    if (hamburgerBtn) hamburgerBtn.addEventListener('click', openMenu);
    if (menuCloseBtn) menuCloseBtn.addEventListener('click', closeMenu);

    navItems.forEach(function (item) {
      item.addEventListener('click', function () {
        closeMenu();
      });
    });
  }

  /* =======================================================================
     15. CONSOLE OVERLAY
     ======================================================================= */
  function initConsole() {
    var consoleEl     = qs('.the-console');
    var toggleBtn     = qs('.console-toggle-btn');
    var consoleInput  = qs('.console-input');
    var consoleOutput = qs('.console-output');

    if (!consoleEl || !toggleBtn) return;

    var isOpen = false;

    var consoleTL = gsap.timeline({ paused: true });
    consoleTL.fromTo(consoleEl, {
      opacity: 0,
      scale: 0.95,
      visibility: 'hidden'
    }, {
      opacity: 1,
      scale: 1,
      visibility: 'visible',
      duration: 0.35,
      ease: 'power2.out'
    });

    toggleBtn.addEventListener('click', function () {
      isOpen = !isOpen;
      if (isOpen) {
        consoleTL.play();
        if (consoleInput) consoleInput.focus();
      } else {
        consoleTL.reverse();
      }
    });

    var consoleResponses = [
      'KPR_CORE :: STATUS ONLINE',
      'SCANNING KEEPER DNA... 10,000 UNIQUE STRANDS FOUND',
      'SOLARPUNK GRID :: ENERGY AT 94.7%',
      'NEURAL LINK :: CALIBRATED',
      'KEEPER PROTOCOL v3.2.1 :: ALL SYSTEMS NOMINAL',
      'ACCESSING ARCHIVE... 512 LORE ENTRIES LOADED',
      'QUANTUM MESH :: INTEGRITY 99.8%',
      'WARNING: UNAUTHORIZED ACCESS ATTEMPT BLOCKED',
      'KEEPER VAULT :: SEALED — BIOMETRIC REQUIRED',
      'SIGNAL STRENGTH :: ████████░░ 82%'
    ];

    if (consoleInput) {
      consoleInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          var cmd = consoleInput.value.trim();
          if (!cmd) return;

          appendConsoleLine('> ' + cmd, 'input');
          consoleInput.value = '';

          setTimeout(function () {
            var resp = consoleResponses[Math.floor(Math.random() * consoleResponses.length)];
            appendConsoleLine(resp, 'output');
          }, 300 + Math.random() * 400);
        }
      });
    }

    function appendConsoleLine(text, type) {
      if (!consoleOutput) return;
      var line = document.createElement('div');
      line.className = 'console-line console-line--' + type;
      line.textContent = text;
      consoleOutput.appendChild(line);
      consoleOutput.scrollTop = consoleOutput.scrollHeight;
    }
  }

  /* =======================================================================
     16. AUDIO BUTTON WAVEFORM
     ======================================================================= */
  function initAudioButton() {
    var audioBtn  = qs('.audio-btn');
    var audioBars = qsa('.audio-bar');

    if (!audioBtn || !audioBars.length) return;

    var isPlaying = false;
    var rafId = null;

    function animateBars() {
      audioBars.forEach(function (bar) {
        var h = rand(0.2, 1.0);
        bar.style.transform = 'scaleY(' + h + ')';
      });
      rafId = requestAnimationFrame(animateBars);
    }

    function stopBars() {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
      audioBars.forEach(function (bar) {
        bar.style.transform = 'scaleY(0.2)';
      });
    }

    audioBtn.addEventListener('click', function () {
      isPlaying = !isPlaying;
      audioBtn.classList.toggle('is-playing', isPlaying);
      if (isPlaying) {
        animateBars();
      } else {
        stopBars();
      }
    });
  }

  /* =======================================================================
     17. THREE.JS SCENE
     ======================================================================= */
  function initThreeJS() {
    if (typeof THREE === 'undefined') return;
    var canvas = document.getElementById('three-canvas');
    if (!canvas) return;

    var scene    = new THREE.Scene();
    var camera   = new THREE.PerspectiveCamera(
      75, window.innerWidth / window.innerHeight, 0.1, 1000
    );
    var renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    /* --- Particles --- */
    var particleCount = 2000;
    var particleGeometry = new THREE.BufferGeometry();
    var positions = new Float32Array(particleCount * 3);

    for (var i = 0; i < particleCount; i++) {
      var theta  = Math.random() * Math.PI * 2;
      var phi    = Math.acos(2 * Math.random() - 1);
      var radius = Math.random() * 20;
      positions[i * 3]     = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi);
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var particleMaterial = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.02,
      transparent: true,
      opacity: 0.7,
      sizeAttenuation: true
    });
    var particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    /* --- Crystal --- */
    var crystalGeometry = new THREE.IcosahedronGeometry(1.5, 1);
    var crystalMaterial = new THREE.MeshPhongMaterial({
      color: 0xc0fb50,
      wireframe: true,
      transparent: true,
      opacity: 0.3
    });
    var crystal = new THREE.Mesh(crystalGeometry, crystalMaterial);
    crystal.position.set(0, 0, -5);
    scene.add(crystal);

    /* --- Lighting --- */
    var ambientLight = new THREE.AmbientLight(0x111111);
    scene.add(ambientLight);

    var pointLight1 = new THREE.PointLight(0xc0fb50, 0.5);
    pointLight1.position.set(5, 5, 5);
    scene.add(pointLight1);

    var pointLight2 = new THREE.PointLight(0x8ca6ff, 0.3);
    pointLight2.position.set(-5, -5, 5);
    scene.add(pointLight2);

    /* --- Camera --- */
    camera.position.set(0, 0, 15);

    /* --- ScrollTrigger for camera --- */
    if (typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.create({
        trigger: document.body,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1,
        onUpdate: function (self) {
          camera.position.z = lerp(15, 5, self.progress);
          camera.position.y = Math.sin(self.progress * Math.PI) * 2;
        }
      });
    }

    /* --- Render loop --- */
    var clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);

      var elapsed = clock.getElapsedTime();

      particles.rotation.y = elapsed * 0.03;
      particles.rotation.x = elapsed * 0.01;

      crystal.rotation.x = elapsed * 0.15;
      crystal.rotation.y = elapsed * 0.2;

      renderer.render(scene, camera);
    }
    animate();

    /* --- Resize --- */
    function onResize() {
      var w = window.innerWidth;
      var h = window.innerHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }
    window.addEventListener('resize', onResize);
  }

  /* =======================================================================
     18. SMOOTH SCROLL
     ======================================================================= */
  function initSmoothScroll() {
    document.documentElement.style.scrollBehavior = 'smooth';
  }

  /* =======================================================================
     19. LAUNCH SECTION
     ======================================================================= */
  function initLaunchSection() {
    var wordmark = qs('.launch-wordmark');
    if (wordmark) {
      var text = wordmark.textContent;
      wordmark.innerHTML = '';
      text.split('').forEach(function (ch) {
        var span = document.createElement('span');
        span.textContent = ch;
        span.style.display = 'inline-block';
        span.style.opacity = '0';
        span.style.transform = 'translateY(20px)';
        if (ch === ' ') span.style.width = '0.3em';
        wordmark.appendChild(span);
      });

      ScrollTrigger.create({
        trigger: wordmark,
        start: 'top 85%',
        once: true,
        onEnter: function () {
          gsap.to(wordmark.querySelectorAll('span'), {
            opacity: 1,
            y: 0,
            duration: 0.08,
            ease: 'power1.out',
            stagger: 0.05
          });
        }
      });
    }

    var floatingCards = qsa('.launch-card, .floating-card');
    floatingCards.forEach(function (card) {
      var speed = parseFloat(card.dataset.speed) || 0.3;
      gsap.fromTo(card, {
        y: 60,
        scale: 0.8,
        opacity: 0
      }, {
        y: 0,
        scale: 1,
        opacity: 1,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: card,
          start: 'top 90%',
          toggleActions: 'play none none none',
          once: true
        }
      });

      gsap.fromTo(card, { y: -30 * speed }, {
        y: 30 * speed,
        ease: 'none',
        scrollTrigger: {
          trigger: card,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true
        }
      });
    });
  }

  /* =======================================================================
     20. FOOTER
     ======================================================================= */
  function initFooter() {
    var footerLogo = qs('.footer-logo');
    if (footerLogo) {
      gsap.fromTo(footerLogo, { y: 40 }, {
        y: -20,
        ease: 'none',
        scrollTrigger: {
          trigger: footerLogo,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true
        }
      });
    }

    qsa('.footer-nav-link').forEach(function (link) {
      link.addEventListener('mouseenter', function () {
        gsap.to(link, { x: 6, duration: 0.25, ease: 'power2.out' });
      });
      link.addEventListener('mouseleave', function () {
        gsap.to(link, { x: 0, duration: 0.25, ease: 'power2.out' });
      });
    });
  }

  /* =======================================================================
     21. PAGE INITIALIZATION
     ======================================================================= */
  function init() {
    initSmoothScroll();
    initPreloader();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* --- Delayed inits that depend on full DOM + preloader --- */
  function onPreloaderDoneExtras() {
    initLaunchSection();
    initFooter();
  }

  var _origOnPreloaderDone = onPreloaderDone;
  onPreloaderDone = function () {
    _origOnPreloaderDone();
    onPreloaderDoneExtras();
  };

})();
'''
