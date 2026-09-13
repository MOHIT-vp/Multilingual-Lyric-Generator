"""HTML section builders for the KPR (Keepers) website.

Each function returns a complete HTML string for a section of the page.
Functions that render images accept an ``images`` dict whose keys are:
    'keeper_hero', 'keeper_gallery', 'cityscape', 'kai_crystal',
    'keeper_eye', 'world_temple', 'keeper_side'
and whose values are base64 data-URI strings.
"""

from kpr.assets import (
    ICON_KPR_MARK,
    ICON_KPR_WORDMARK,
    ICON_HAMBURGER,
    ICON_CLOSE,
    ICON_ARROW_DOWN,
    ICON_ARROW_UP,
    ICON_SCROLL_ARROW,
    ICON_PLAY,
    ICON_CROSSHAIR,
    ICON_CONSOLE,
    ICON_DOUBLE_ARROW,
    ICON_OPENSEA,
    ICON_TWITTER,
    ICON_DISCORD,
    ICON_DOWNLOAD,
)


# =========================================================================== #
#  1. Preloader
# =========================================================================== #

def preloader_html() -> str:
    """Fixed overlay preloader with progress bar, percentage, and file list."""
    return f'''
<!-- ====== PRELOADER ====== -->
<div id="preloader" class="preloader" aria-label="Loading">
  <div class="preloader__inner">

    <!-- Loading triangle icon -->
    <div class="preloader__icon">
      <svg width="32" height="28" viewBox="0 0 32 28" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M16 0L32 28H0L16 0Z" fill="#000"/>
      </svg>
    </div>

    <!-- Progress bar -->
    <div class="preloader__bar-wrap">
      <div class="preloader__bar">
        <div class="preloader__bar-fill" id="preloaderBarFill"></div>
      </div>
    </div>

    <!-- Label + percentage -->
    <div class="preloader__info">
      <span class="preloader__label">LOADING</span>
      <span class="preloader__pct" id="preloaderPct">0%</span>
    </div>

    <!-- File list (monospace, fades in/out) -->
    <div class="preloader__files" id="preloaderFiles">
      <p class="preloader__file preloader__file--active">initializing keeper protocol…</p>
      <p class="preloader__file">loading typefaces [ABCWhyte, Inter]…</p>
      <p class="preloader__file">decoding image assets…</p>
      <p class="preloader__file">compiling shader modules…</p>
      <p class="preloader__file">connecting to mainnet…</p>
      <p class="preloader__file">building scene graph…</p>
      <p class="preloader__file">calibrating scroll triggers…</p>
      <p class="preloader__file">keeper protocol ready.</p>
    </div>

  </div>
</div>
'''


# =========================================================================== #
#  2. Canvas Container
# =========================================================================== #

def canvas_container_html() -> str:
    """Fixed full-viewport canvas for WebGL / Three.js background."""
    return '''
<!-- ====== CANVAS ====== -->
<div id="canvas-container" class="canvas-container">
  <canvas id="three-canvas"></canvas>
</div>
'''


# =========================================================================== #
#  3. Frame (persistent UI chrome)
# =========================================================================== #

def frame_html() -> str:
    """Persistent frame with navigation, logo, audio controls for desktop."""
    return f'''
<!-- ====== FRAME ====== -->

<!-- Light-theme frame (visible on light sections) -->
<div class="the-frame the-frame--light" id="frameLightEl" data-theme="light">
  <!-- Top bar -->
  <div class="the-frame__top">
    <div class="the-frame__top-left">
      <button class="the-frame__hamburger js-menu-open" id="menuOpenLight" aria-label="Open menu">
        {ICON_HAMBURGER}
      </button>
    </div>
    <div class="the-frame__top-center">
      <div class="the-frame-progress">
        <div class="the-frame-progress__track">
          <div class="the-frame-progress__fill" id="frameProgressFillLight"></div>
        </div>
      </div>
      <nav class="the-frame__submenu" aria-label="Section navigation">
        <a href="#home-project-intro" class="the-frame__submenu-link js-submenu-link" data-section-target="home-project-intro">PROJECT</a>
        <a href="#home-collection-intro" class="the-frame__submenu-link js-submenu-link" data-section-target="home-collection-intro">THE KEEP</a>
        <a href="#home-tableau-factions" class="the-frame__submenu-link js-submenu-link" data-section-target="home-tableau-factions">FACTIONS</a>
        <a href="#home-tableau-world" class="the-frame__submenu-link js-submenu-link" data-section-target="home-tableau-world">THE WORLD</a>
      </nav>
    </div>
    <div class="the-frame__top-right">
      <button class="the-frame__signin" id="signinBtnLight">SIGN IN</button>
    </div>
  </div>

  <!-- Left sidebar -->
  <div class="the-frame__sidebar">
    <div class="the-frame__sidebar-top">
      <a href="#" class="the-frame__logo" aria-label="KPR home">
        {ICON_KPR_MARK}
      </a>
    </div>
    <div class="the-frame__sidebar-bottom">
      <button class="the-frame__audio js-audio-toggle" id="audioToggleLight" aria-label="Toggle audio">
        <span class="audio-bars">
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
        </span>
      </button>
      <button class="the-frame__console-btn js-console-open" id="consoleOpenLight" aria-label="Open console">
        {ICON_CONSOLE}
      </button>
    </div>
  </div>

  <!-- Outer border -->
  <div class="the-frame__border"></div>
</div>

<!-- Dark-theme frame (visible on dark sections) -->
<div class="the-frame the-frame--dark" id="frameDarkEl" data-theme="dark">
  <!-- Top bar -->
  <div class="the-frame__top">
    <div class="the-frame__top-left">
      <button class="the-frame__hamburger js-menu-open" id="menuOpenDark" aria-label="Open menu">
        {ICON_HAMBURGER}
      </button>
    </div>
    <div class="the-frame__top-center">
      <div class="the-frame-progress">
        <div class="the-frame-progress__track">
          <div class="the-frame-progress__fill" id="frameProgressFillDark"></div>
        </div>
      </div>
      <nav class="the-frame__submenu" aria-label="Section navigation">
        <a href="#home-project-intro" class="the-frame__submenu-link js-submenu-link" data-section-target="home-project-intro">PROJECT</a>
        <a href="#home-collection-intro" class="the-frame__submenu-link js-submenu-link" data-section-target="home-collection-intro">THE KEEP</a>
        <a href="#home-tableau-factions" class="the-frame__submenu-link js-submenu-link" data-section-target="home-tableau-factions">FACTIONS</a>
        <a href="#home-tableau-world" class="the-frame__submenu-link js-submenu-link" data-section-target="home-tableau-world">THE WORLD</a>
      </nav>
    </div>
    <div class="the-frame__top-right">
      <button class="the-frame__signin" id="signinBtnDark">SIGN IN</button>
    </div>
  </div>

  <!-- Left sidebar -->
  <div class="the-frame__sidebar">
    <div class="the-frame__sidebar-top">
      <a href="#" class="the-frame__logo" aria-label="KPR home">
        {ICON_KPR_MARK}
      </a>
    </div>
    <div class="the-frame__sidebar-bottom">
      <button class="the-frame__audio js-audio-toggle" id="audioToggleDark" aria-label="Toggle audio">
        <span class="audio-bars">
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
          <span class="audio-bars__bar"></span>
        </span>
      </button>
      <button class="the-frame__console-btn js-console-open" id="consoleOpenDark" aria-label="Open console">
        {ICON_CONSOLE}
      </button>
    </div>
  </div>

  <!-- Outer border -->
  <div class="the-frame__border"></div>
</div>
'''


# =========================================================================== #
#  4. Mobile Nav
# =========================================================================== #

def nav_mobile_html() -> str:
    """Fixed top bar for mobile viewports."""
    return f'''
<!-- ====== MOBILE NAV ====== -->
<div class="nav-mobile" id="navMobile">
  <div class="nav-mobile__left">
    <button class="nav-mobile__hamburger js-menu-open" id="menuOpenMobile" aria-label="Open menu">
      {ICON_HAMBURGER}
    </button>
  </div>
  <div class="nav-mobile__center">
    <a href="#" class="nav-mobile__wordmark" aria-label="KPR home">
      {ICON_KPR_WORDMARK}
    </a>
  </div>
  <div class="nav-mobile__right">
    <button class="nav-mobile__signin" id="signinBtnMobile">SIGN IN</button>
  </div>
</div>
'''


# =========================================================================== #
#  5. Menu (fullscreen overlay)
# =========================================================================== #

def menu_html() -> str:
    """Full-screen overlay navigation menu."""
    return f'''
<!-- ====== MENU ====== -->
<div class="the-menu" id="theMenu" aria-hidden="true" role="dialog" aria-label="Main navigation">
  <div class="the-menu__backdrop"></div>

  <div class="the-menu__inner">
    <!-- Left panel -->
    <div class="the-menu__panel">

      <!-- Discover section -->
      <div class="the-menu__section">
        <span class="the-menu__label">DISCOVER</span>
        <nav class="the-menu__nav" aria-label="Main navigation">
          <a href="#home-landing" class="the-menu__nav-item js-menu-nav is-active" data-section-target="home-landing" data-page="001">
            <span class="the-menu__nav-text">PROJECT</span>
            <span class="the-menu__nav-page">PAGE 001</span>
          </a>
          <a href="#home-collection-intro" class="the-menu__nav-item js-menu-nav" data-section-target="home-collection-intro" data-page="002">
            <span class="the-menu__nav-text">THE KEEP</span>
            <span class="the-menu__nav-page">PAGE 002</span>
          </a>
          <a href="#home-tableau-factions" class="the-menu__nav-item js-menu-nav" data-section-target="home-tableau-factions" data-page="003">
            <span class="the-menu__nav-text">FACTIONS</span>
            <span class="the-menu__nav-page">PAGE 003</span>
          </a>
          <a href="#home-tableau-world" class="the-menu__nav-item js-menu-nav" data-section-target="home-tableau-world" data-page="004">
            <span class="the-menu__nav-text">THE WORLD</span>
            <span class="the-menu__nav-page">PAGE 004</span>
          </a>
          <a href="#" class="the-menu__nav-item js-menu-nav" data-page="005">
            <span class="the-menu__nav-text">JOURNAL</span>
            <span class="the-menu__nav-page">PAGE 005</span>
          </a>
          <a href="#" class="the-menu__nav-item js-menu-nav" data-page="006">
            <span class="the-menu__nav-text">ABOUT</span>
            <span class="the-menu__nav-page">PAGE 006</span>
          </a>
        </nav>
      </div>

      <!-- Connect section -->
      <div class="the-menu__section the-menu__section--connect">
        <span class="the-menu__label">CONNECT</span>
        <div class="the-menu__social">
          <a href="https://twitter.com/kaboraworld" class="the-menu__social-link" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
            {ICON_TWITTER}
            <span>TWITTER</span>
          </a>
          <a href="https://discord.gg/keepers" class="the-menu__social-link" target="_blank" rel="noopener noreferrer" aria-label="Discord">
            {ICON_DISCORD}
            <span>DISCORD</span>
          </a>
        </div>
      </div>

      <!-- Buy on section -->
      <div class="the-menu__section the-menu__section--buy">
        <span class="the-menu__label">BUY ON</span>
        <a href="https://opensea.io/collection/keepers" class="the-menu__opensea-btn" target="_blank" rel="noopener noreferrer">
          {ICON_OPENSEA}
          <span>OPENSEA</span>
        </a>
      </div>

      <!-- Bottom bar -->
      <div class="the-menu__bottom">
        <div class="the-menu__lang">
          <button class="the-menu__lang-btn is-active">EN</button>
          <button class="the-menu__lang-btn">JA</button>
          <button class="the-menu__lang-btn">KR</button>
        </div>
        <span class="the-menu__copyright">&copy; 2022 KEEPERS</span>
        <div class="the-menu__live">
          <span class="the-menu__live-dot"></span>
          <span class="the-menu__live-text">LIVE</span>
          <span class="the-menu__live-count" id="menuLiveCount">2,847</span>
        </div>
      </div>

    </div>

    <!-- Right sidebar -->
    <div class="the-menu__sidebar">
      <button class="the-menu__close js-menu-close" id="menuCloseBtn" aria-label="Close menu">
        {ICON_CLOSE}
      </button>
      <div class="the-menu__sidebar-logo">
        {ICON_KPR_MARK}
      </div>
      <div class="the-menu__sidebar-controls">
        <button class="the-menu__audio js-audio-toggle" aria-label="Toggle audio">
          <span class="audio-bars">
            <span class="audio-bars__bar"></span>
            <span class="audio-bars__bar"></span>
            <span class="audio-bars__bar"></span>
            <span class="audio-bars__bar"></span>
            <span class="audio-bars__bar"></span>
          </span>
        </button>
        <button class="the-menu__console-btn js-console-open" aria-label="Open console">
          {ICON_CONSOLE}
        </button>
      </div>
    </div>
  </div>
</div>
'''


# =========================================================================== #
#  6. Landing (Section 1)
# =========================================================================== #

def landing_html(images: dict) -> str:
    """Hero landing with large KPR typography and scroll indicator."""
    return f'''
<!-- ====== SECTION 1 — LANDING ====== -->
<section class="section section--light home-landing" id="home-landing"
         data-section="landing" data-theme="light" data-section-index="1">
  <div class="home-landing__inner">

    <!-- Description text (top-left) -->
    <div class="home-landing__description">
      <p class="home-landing__desc-text">
        KPR IS A BRAND THAT FOCUSES ON COLLECTIVE NARRATIVE AND COMMUNITY-DRIVEN
        STORYTELLING. A NEW GENERATION OF DIGITAL COLLECTIBLES THAT BRIDGE ART,
        TECHNOLOGY, AND CULTURE.
      </p>
    </div>

    <!-- Large display typography -->
    <div class="home-landing__titles">
      <div class="home-landing__title-row">
        <div class="word-reveal">
          <span class="home-landing__title-line">
            <sup class="home-landing__sup">01</sup><span class="home-landing__letter-accent">K</span>EEP.
          </span>
        </div>
      </div>
      <div class="home-landing__title-row">
        <div class="word-reveal">
          <span class="home-landing__title-line">
            <sup class="home-landing__sup">02</sup><span class="home-landing__letter-accent">P</span>ROTECT.
          </span>
        </div>
      </div>
      <div class="home-landing__title-row">
        <div class="word-reveal">
          <span class="home-landing__title-line">
            <sup class="home-landing__sup">03</sup><span class="home-landing__letter-accent">R</span>EIMAGINE.
          </span>
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <div class="home-landing__scroll" id="scrollIndicator">
      <span class="home-landing__scroll-label">SCROLL</span>
      <span class="home-landing__scroll-icon">
        {ICON_SCROLL_ARROW}
      </span>
    </div>

  </div>
</section>
'''


# =========================================================================== #
#  7. Project Intro (Section 2)
# =========================================================================== #

def project_intro_html(images: dict) -> str:
    """Project intro with two-column grid, hero image, and play button."""
    return f'''
<!-- ====== SECTION 2 — PROJECT INTRO ====== -->
<section class="section section--dark home-project-intro" id="home-project-intro"
         data-section="project-intro" data-theme="dark" data-section-index="2">
  <div class="home-project-intro__inner">

    <div class="home-project-intro__grid">

      <!-- Left column -->
      <div class="home-project-intro__left">
        <div class="dot-caption">
          <span class="dot-caption__dot"></span>
          <span class="dot-caption__text">001</span>
        </div>

        <h2 class="home-project-intro__heading">
          <div class="word-reveal"><span>A FAMILIAR</span></div>
          <div class="word-reveal"><span>WORLD&hellip;</span></div>
          <div class="word-reveal"><span>SET ON A</span></div>
          <div class="word-reveal"><span>DIFFERENT</span></div>
          <div class="word-reveal"><span>PATH.</span></div>
        </h2>

        <div class="home-project-intro__side-image" data-parallax data-speed="0.15">
          <img src="{images.get('keeper_side', '')}" alt="Animus character, side profile"
               class="home-project-intro__side-img" loading="lazy" />
          <span class="home-project-intro__side-caption">ANIMUS CHARACTER</span>
        </div>
      </div>

      <!-- Right column -->
      <div class="home-project-intro__right">
        <div class="home-project-intro__hero-image" data-parallax data-speed="0.1">
          <img src="{images.get('keeper_hero', '')}" alt="Keeper hero character"
               class="home-project-intro__hero-img" loading="lazy" />
          <button class="home-project-intro__play-btn js-play-trailer" id="playTrailerBtn" aria-label="Play trailer">
            {ICON_PLAY}
          </button>
          <span class="home-project-intro__hero-caption">TRAILER V.004</span>
        </div>
      </div>

    </div>

    <!-- Body text -->
    <div class="home-project-intro__body">
      <hr class="js-line" />
      <div class="home-project-intro__body-text">
        <p>
          ISOLATED WITHIN THE NEW EDEN SAFE ZONE, HUMANITY HAS FORGOTTEN THE
          WORLD THAT ONCE WAS. BUT BEYOND THE WALLS, THE KEEPERS REMEMBER.
          THEY ARE THE LAST LINE BETWEEN ORDER AND OBLIVION — GUARDIANS OF
          FORGOTTEN KNOWLEDGE, WIELDING ANCIENT TECHNOLOGY THAT THE CORPORATIONS
          TRIED TO ERASE.
        </p>
        <p>
          YOUR KEEPER IS YOUR IDENTITY IN THIS WORLD. A UNIQUE DIGITAL CHARACTER
          THAT CARRIES YOUR STORY, YOUR CHOICES, AND YOUR LEGACY FORWARD.
        </p>
      </div>
      <hr class="js-line" />
    </div>

  </div>
</section>
'''


# =========================================================================== #
#  8. Project Story (Section 3)
# =========================================================================== #

def project_story_html(images: dict) -> str:
    """Story section with terminal text, coordinates, and diagonal lines."""
    return f'''
<!-- ====== SECTION 3 — PROJECT STORY ====== -->
<section class="section section--light home-project-story" id="home-project-story"
         data-section="project-story" data-theme="light" data-section-index="3">
  <div class="home-project-story__inner">

    <!-- Row 1 -->
    <div class="home-project-story__row home-project-story__row--1">
      <div class="home-project-story__row-left">
        <div class="dot-caption">
          <span class="dot-caption__dot"></span>
          <span class="dot-caption__text">002</span>
        </div>
        <h2 class="home-project-story__heading">
          <div class="word-reveal"><span>YOU ARE</span></div>
          <div class="word-reveal"><span>A KEEPER.</span></div>
          <div class="word-reveal"><span>A GUARDIAN</span></div>
          <div class="word-reveal"><span>OF WHAT WAS</span></div>
          <div class="word-reveal"><span>LOST.</span></div>
        </h2>
      </div>
      <div class="home-project-story__row-right">
        <div class="home-project-story__terminal">
          <div class="home-project-story__terminal-header">
            <span class="home-project-story__terminal-dot"></span>
            <span class="home-project-story__terminal-dot"></span>
            <span class="home-project-story__terminal-dot"></span>
          </div>
          <div class="home-project-story__terminal-body">
            <p class="hacky-text" data-final-text="KEEPER PROTOCOL v4.2.1 — STATUS: ACTIVE">
              KEEPER PROTOCOL v4.2.1 — STATUS: ACTIVE
            </p>
            <p class="hacky-text" data-final-text="SCANNING SECTOR 7G... ANOMALY DETECTED">
              SCANNING SECTOR 7G... ANOMALY DETECTED
            </p>
            <p class="hacky-text" data-final-text="> INITIATING SEQUENCE: REMEMBER">
              &gt; INITIATING SEQUENCE: REMEMBER
            </p>
            <p class="hacky-text" data-final-text="> THE OLD WORLD CALLS TO YOU.">
              &gt; THE OLD WORLD CALLS TO YOU.
            </p>
            <span class="home-project-story__terminal-cursor"></span>
          </div>
        </div>
      </div>
    </div>

    <hr class="js-line" />

    <!-- Row 2 — Coordinates + topographic pattern -->
    <div class="home-project-story__row home-project-story__row--2">
      <div class="home-project-story__coords">
        <span class="home-project-story__coord-label">COORDINATES</span>
        <span class="home-project-story__coord-value">N 35&deg;27.37 / E 139&deg;38.57</span>
      </div>
      <div class="home-project-story__topographic">
        <svg class="home-project-story__topo-svg" viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M0 100 Q50 60 100 100 T200 100 T300 100 T400 100" stroke="currentColor" stroke-width="0.5" fill="none" opacity="0.3"/>
          <path d="M0 120 Q50 80 100 120 T200 120 T300 120 T400 120" stroke="currentColor" stroke-width="0.5" fill="none" opacity="0.25"/>
          <path d="M0 80 Q50 40 100 80 T200 80 T300 80 T400 80" stroke="currentColor" stroke-width="0.5" fill="none" opacity="0.2"/>
          <path d="M0 140 Q50 100 100 140 T200 140 T300 140 T400 140" stroke="currentColor" stroke-width="0.5" fill="none" opacity="0.15"/>
          <path d="M0 60 Q50 20 100 60 T200 60 T300 60 T400 60" stroke="currentColor" stroke-width="0.5" fill="none" opacity="0.15"/>
          <circle cx="200" cy="100" r="3" fill="currentColor" opacity="0.5"/>
          <line x1="200" y1="90" x2="200" y2="110" stroke="currentColor" stroke-width="0.5" opacity="0.5"/>
          <line x1="190" y1="100" x2="210" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.5"/>
        </svg>
      </div>
    </div>

    <hr class="js-line" />

    <!-- Row 3 — Diagonal + heading -->
    <div class="home-project-story__row home-project-story__row--3">
      <div class="home-project-story__diagonal">
        <svg class="home-project-story__diag-svg" viewBox="0 0 100 200" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <line x1="0" y1="200" x2="100" y2="0" stroke="currentColor" stroke-width="0.5"/>
        </svg>
      </div>
      <div class="home-project-story__row3-content">
        <div class="dot-caption">
          <span class="dot-caption__dot"></span>
          <span class="dot-caption__text">003</span>
        </div>
        <h2 class="home-project-story__heading home-project-story__heading--alt">
          <div class="word-reveal"><span>WHAT WILL</span></div>
          <div class="word-reveal"><span>YOU DO WITH</span></div>
          <div class="word-reveal"><span>THIS POWER?</span></div>
          <div class="word-reveal"><span>HOW WILL</span></div>
          <div class="word-reveal"><span>YOU SHAPE</span></div>
          <div class="word-reveal"><span>THE WORLD</span></div>
          <div class="word-reveal"><span>THAT COMES</span></div>
          <div class="word-reveal"><span>NEXT?</span></div>
        </h2>
      </div>
    </div>

    <hr class="js-line" />

  </div>
</section>
'''


# =========================================================================== #
#  9. Collection Intro (Section 4)
# =========================================================================== #

def collection_intro_html(images: dict) -> str:
    """Three-column collection intro with counter, hero, and detail images."""
    return f'''
<!-- ====== SECTION 4 — COLLECTION INTRO ====== -->
<section class="section section--dark home-collection-intro" id="home-collection-intro"
         data-section="collection-intro" data-theme="dark" data-section-index="4">
  <div class="home-collection-intro__inner">

    <div class="home-collection-intro__grid">

      <!-- Left: counter -->
      <div class="home-collection-intro__left">
        <div class="home-collection-intro__counter">
          <span class="home-collection-intro__counter-num" id="collectionCounter">10K</span>
        </div>
        <div class="home-collection-intro__counter-label">INITIAL COLLECTION</div>
        <div class="home-collection-intro__counter-arrow">
          {ICON_DOUBLE_ARROW}
        </div>
      </div>

      <!-- Center: hero character -->
      <div class="home-collection-intro__center">
        <div class="home-collection-intro__hero-wrap" data-parallax data-speed="0.08">
          <img src="{images.get('keeper_hero', '')}" alt="Keeper hero — full body"
               class="home-collection-intro__hero-img" loading="lazy" />
        </div>
      </div>

      <!-- Right: detail images -->
      <div class="home-collection-intro__right">
        <div class="home-collection-intro__detail home-collection-intro__detail--top">
          <img src="{images.get('kai_crystal', '')}" alt="Kai Crystal artifact"
               class="home-collection-intro__detail-img" loading="lazy" />
          <span class="home-collection-intro__detail-caption">KAI CRYSTAL — POWER SOURCE</span>
        </div>
        <div class="home-collection-intro__detail home-collection-intro__detail--bottom">
          <img src="{images.get('keeper_eye', '')}" alt="Keeper eye closeup"
               class="home-collection-intro__detail-img" loading="lazy" />
          <span class="home-collection-intro__detail-caption">ENHANCED OPTICS — GEN 4</span>
        </div>
      </div>

    </div>

  </div>
</section>
'''


# =========================================================================== #
#  10. Collection Gallery (Section 5)
# =========================================================================== #

def collection_gallery_html(images: dict) -> str:
    """Gallery section with overlapping perspective cards."""
    return f'''
<!-- ====== SECTION 5 — COLLECTION GALLERY ====== -->
<section class="section section--dark home-collection-gallery" id="home-collection-gallery"
         data-section="collection-gallery" data-theme="dark" data-section-index="5">
  <div class="home-collection-gallery__inner">

    <!-- Top row -->
    <div class="home-collection-gallery__header">
      <div class="home-collection-gallery__header-left">
        <div class="dot-caption">
          <span class="dot-caption__dot"></span>
          <span class="dot-caption__text">004</span>
        </div>
        <h2 class="home-collection-gallery__heading">
          <div class="word-reveal"><span>10,000 UNIQUE</span></div>
          <div class="word-reveal"><span>DIGITAL</span></div>
          <div class="word-reveal"><span>COLLECTIBLES.</span></div>
        </h2>
      </div>
      <div class="home-collection-gallery__header-right">
        <div class="dot-caption">
          <span class="dot-caption__dot"></span>
          <span class="dot-caption__text">INITIAL COLLECTION</span>
        </div>
        <p class="home-collection-gallery__desc">
          EACH KEEPER IS A PROCEDURALLY GENERATED, ONE-OF-A-KIND CHARACTER
          WITH OVER 200 HAND-CRAFTED TRAITS. YOUR KEEPER IS YOUR KEY TO THE
          WORLD — YOUR AVATAR, YOUR IDENTITY, YOUR STORY.
        </p>
      </div>
    </div>

    <hr class="js-line" />

    <!-- Gallery grid -->
    <div class="home-collection-gallery__grid" id="galleryGrid">
      <div class="home-collection-gallery__card home-collection-gallery__card--1" data-parallax data-speed="0.05">
        <img src="{images.get('keeper_gallery', '')}" alt="Keeper #2741" loading="lazy" />
        <span class="home-collection-gallery__card-id">#2741</span>
      </div>
      <div class="home-collection-gallery__card home-collection-gallery__card--2" data-parallax data-speed="0.12">
        <img src="{images.get('keeper_hero', '')}" alt="Keeper #0087" loading="lazy" />
        <span class="home-collection-gallery__card-id">#0087</span>
      </div>
      <div class="home-collection-gallery__card home-collection-gallery__card--3" data-parallax data-speed="0.08">
        <img src="{images.get('keeper_gallery', '')}" alt="Keeper #5190" loading="lazy" />
        <span class="home-collection-gallery__card-id">#5190</span>
      </div>
      <div class="home-collection-gallery__card home-collection-gallery__card--4" data-parallax data-speed="0.15">
        <img src="{images.get('keeper_hero', '')}" alt="Keeper #1337" loading="lazy" />
        <span class="home-collection-gallery__card-id">#1337</span>
      </div>
      <div class="home-collection-gallery__card home-collection-gallery__card--5" data-parallax data-speed="0.1">
        <img src="{images.get('keeper_gallery', '')}" alt="Keeper #9002" loading="lazy" />
        <span class="home-collection-gallery__card-id">#9002</span>
      </div>
    </div>

  </div>
</section>
'''


# =========================================================================== #
#  11. Tableau Sections (Sections 6-8)
# =========================================================================== #

def tableau_sections_html(images: dict) -> str:
    """Three sticky tableau sections: The Keep, Factions, The World."""
    return f'''
<!-- ====== SECTION 6 — TABLEAU: THE KEEP ====== -->
<section class="section section--dark home-tableau home-tableau--keep" id="home-tableau-keep"
         data-section="tableau-keep" data-theme="dark" data-section-index="6">
  <div class="home-tableau__sticky">

    <!-- Background layer -->
    <div class="sd-layer" data-parallax-bg data-speed="0.03">
      <div class="sd-layer__image" style="background-image:url('{images.get('cityscape', '')}');"></div>
      <div class="sd-layer__overlay"></div>
    </div>

    <!-- Title shell -->
    <div class="sd-layer-shell">
      <div class="sd-layer-shell__inner">
        <span class="sd-layer-shell__caption">MOST NEEDED</span>
        <h2 class="sd-layer-shell__title">
          <span class="sd-layer-shell__title-line">THE /</span>
          <span class="sd-layer-shell__title-line sd-layer-shell__title-line--large">KEEP</span>
        </h2>
      </div>
    </div>

    <!-- Hold button -->
    <div class="btn-hold" id="btnHoldKeep">
      <button class="btn-hold__btn js-btn-hold" data-target="tableau-keep-story" aria-label="Click and hold to reveal">
        {ICON_CROSSHAIR}
      </button>
      <span class="btn-hold__label">CLICK &amp; HOLD</span>
      <svg class="btn-hold__progress" width="80" height="80" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r="36" fill="none" stroke="currentColor" stroke-width="1" opacity="0.2"/>
        <circle class="btn-hold__progress-ring" cx="40" cy="40" r="36" fill="none" stroke="currentColor"
                stroke-width="2" stroke-dasharray="226.2" stroke-dashoffset="226.2"
                transform="rotate(-90 40 40)"/>
      </svg>
    </div>

    <!-- Story overlay -->
    <div class="tableau-story" id="tableau-keep-story" aria-hidden="true">
      <div class="tableau-story__inner">
        <p class="tableau-story__text">
          THE KEEP IS THE LAST BASTION. A FORTRESS BUILT FROM THE RUINS OF THE OLD WORLD,
          WHERE KEEPERS GATHER TO SHARE KNOWLEDGE, TRAIN, AND PREPARE FOR WHAT LIES AHEAD.
          WITHIN ITS WALLS, ANCIENT SERVERS HUM WITH DATA FROM A CIVILIZATION THAT CHOSE TO
          FORGET. HERE, NOTHING IS FORGOTTEN.
        </p>
        <span class="tableau-story__tag">SECTION 001 — SANCTUARY</span>
      </div>
    </div>

  </div>
</section>

<!-- ====== SECTION 7 — TABLEAU: FACTIONS ====== -->
<section class="section section--dark home-tableau home-tableau--factions" id="home-tableau-factions"
         data-section="tableau-factions" data-theme="dark" data-section-index="7">
  <div class="home-tableau__sticky">

    <!-- Background layer -->
    <div class="sd-layer" data-parallax-bg data-speed="0.03">
      <div class="sd-layer__image" style="background-image:url('{images.get('cityscape', '')}');"></div>
      <div class="sd-layer__overlay sd-layer__overlay--factions"></div>
    </div>

    <!-- Title shell -->
    <div class="sd-layer-shell">
      <div class="sd-layer-shell__inner">
        <span class="sd-layer-shell__caption">DIVIDED</span>
        <h2 class="sd-layer-shell__title">
          <span class="sd-layer-shell__title-line">2 /</span>
          <span class="sd-layer-shell__title-line sd-layer-shell__title-line--large">FACTIONS</span>
        </h2>
      </div>
    </div>

    <!-- Hold button -->
    <div class="btn-hold" id="btnHoldFactions">
      <button class="btn-hold__btn js-btn-hold" data-target="tableau-factions-story" aria-label="Click and hold to reveal">
        {ICON_CROSSHAIR}
      </button>
      <span class="btn-hold__label">CLICK &amp; HOLD</span>
      <svg class="btn-hold__progress" width="80" height="80" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r="36" fill="none" stroke="currentColor" stroke-width="1" opacity="0.2"/>
        <circle class="btn-hold__progress-ring" cx="40" cy="40" r="36" fill="none" stroke="currentColor"
                stroke-width="2" stroke-dasharray="226.2" stroke-dashoffset="226.2"
                transform="rotate(-90 40 40)"/>
      </svg>
    </div>

    <!-- Story overlay -->
    <div class="tableau-story" id="tableau-factions-story" aria-hidden="true">
      <div class="tableau-story__inner">
        <p class="tableau-story__text">
          TWO FACTIONS HAVE EMERGED FROM THE ASHES. THE SOLARI SEEK TO REBUILD —
          HARNESSING SOLAR ENERGY AND BIOTECH TO CREATE A NEW EDEN. THE UMBRAL
          BELIEVE THE ONLY WAY FORWARD IS THROUGH — EMBRACING THE MACHINE,
          AUGMENTING BEYOND RECOGNITION. BOTH CARRY TRUTH. BOTH CARRY DANGER.
          YOUR ALLEGIANCE WILL SHAPE EVERYTHING.
        </p>
        <span class="tableau-story__tag">SECTION 002 — ALLEGIANCE</span>
      </div>
    </div>

  </div>
</section>

<!-- ====== SECTION 8 — TABLEAU: THE WORLD ====== -->
<section class="section section--dark home-tableau home-tableau--world" id="home-tableau-world"
         data-section="tableau-world" data-theme="dark" data-section-index="8">
  <div class="home-tableau__sticky">

    <!-- Background layer -->
    <div class="sd-layer" data-parallax-bg data-speed="0.03">
      <div class="sd-layer__image" style="background-image:url('{images.get('world_temple', '')}');"></div>
      <div class="sd-layer__overlay sd-layer__overlay--world"></div>
    </div>

    <!-- Title shell -->
    <div class="sd-layer-shell">
      <div class="sd-layer-shell__inner">
        <span class="sd-layer-shell__caption">WHOLE NEW</span>
        <h2 class="sd-layer-shell__title">
          <span class="sd-layer-shell__title-line">A WHOLE NEW /</span>
          <span class="sd-layer-shell__title-line sd-layer-shell__title-line--large">WORLD</span>
        </h2>
      </div>
    </div>

    <!-- Hold button -->
    <div class="btn-hold" id="btnHoldWorld">
      <button class="btn-hold__btn js-btn-hold" data-target="tableau-world-story" aria-label="Click and hold to reveal">
        {ICON_CROSSHAIR}
      </button>
      <span class="btn-hold__label">CLICK &amp; HOLD</span>
      <svg class="btn-hold__progress" width="80" height="80" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r="36" fill="none" stroke="currentColor" stroke-width="1" opacity="0.2"/>
        <circle class="btn-hold__progress-ring" cx="40" cy="40" r="36" fill="none" stroke="currentColor"
                stroke-width="2" stroke-dasharray="226.2" stroke-dashoffset="226.2"
                transform="rotate(-90 40 40)"/>
      </svg>
    </div>

    <!-- Story overlay -->
    <div class="tableau-story" id="tableau-world-story" aria-hidden="true">
      <div class="tableau-story__inner">
        <p class="tableau-story__text">
          BEYOND NEW EDEN, THE WORLD HAS REWILDED. FORESTS HAVE RECLAIMED THE
          SKYSCRAPERS. CORAL GROWS THROUGH SUBWAY TUNNELS. TEMPLES OF A FORGOTTEN
          AGE STAND SENTINEL OVER VALLEYS OF BIOLUMINESCENT FLORA. THIS IS NOT
          THE END — IT IS A BEGINNING. AND THE KEEPERS ARE THE FIRST TO WALK
          THESE NEW PATHS.
        </p>
        <span class="tableau-story__tag">SECTION 003 — TERRA NOVA</span>
      </div>
    </div>

  </div>
</section>
'''


# =========================================================================== #
#  12. Launch (Section 9)
# =========================================================================== #

def launch_html(images: dict) -> str:
    """Launch section with massive KEEPERS title and floating image cards."""
    return f'''
<!-- ====== SECTION 9 — LAUNCH ====== -->
<section class="section section--dark home-launch" id="home-launch"
         data-section="launch" data-theme="dark" data-section-index="9">
  <div class="home-launch__inner">

    <hr class="js-line" />

    <!-- Massive title -->
    <div class="home-launch__title-wrap">
      <h2 class="home-launch__title">
        <div class="word-reveal"><span>KEEPERS</span></div>
      </h2>
    </div>

    <!-- Floating image cards -->
    <div class="home-launch__cards">
      <div class="home-launch__card home-launch__card--1" data-parallax data-speed="0.12">
        <img src="{images.get('world_temple', '')}" alt="World temple ruins" loading="lazy" />
      </div>
      <div class="home-launch__card home-launch__card--2" data-parallax data-speed="0.08">
        <img src="{images.get('keeper_eye', '')}" alt="Keeper enhanced optics" loading="lazy" />
      </div>
      <div class="home-launch__card home-launch__card--3" data-parallax data-speed="0.15">
        <img src="{images.get('keeper_side', '')}" alt="Keeper side profile" loading="lazy" />
      </div>
    </div>

    <!-- Caption + text -->
    <div class="home-launch__content">
      <div class="dot-caption">
        <span class="dot-caption__dot"></span>
        <span class="dot-caption__text">BECOME A KEEPER</span>
      </div>

      <div class="home-launch__body">
        <p>
          THE STORY IS NOT WRITTEN. IT IS LIVED. EVERY DECISION MADE BY EVERY
          KEEPER RIPPLES THROUGH THE NARRATIVE, SHAPING THE WORLD IN REAL TIME.
          THIS IS NOT A STATIC COLLECTION — IT IS A LIVING, BREATHING UNIVERSE
          POWERED BY ITS COMMUNITY.
        </p>
        <p>
          JOIN THE KEEPERS. CHOOSE YOUR FACTION. EXPLORE THE WORLD BEYOND THE
          WALLS. AND HELP US WRITE THE NEXT CHAPTER OF THIS STORY — TOGETHER.
        </p>
      </div>
    </div>

    <hr class="js-line" />

  </div>
</section>
'''


# =========================================================================== #
#  13. Footer
# =========================================================================== #

def footer_html() -> str:
    """Full-width footer with four columns, giant logo, and bottom bar."""
    return f'''
<!-- ====== FOOTER ====== -->
<footer class="the-footer" id="theFooter" data-section="footer" data-theme="dark">
  <div class="the-footer__inner">

    <!-- Four columns -->
    <div class="the-footer__columns">

      <!-- Column 1: Console preview -->
      <div class="the-footer__col the-footer__col--console">
        <div class="the-footer__console-preview">
          <pre class="the-footer__console-text"><span class="the-footer__console-comment">// initializing</span>
<span class="the-footer__console-comment">// new files detected</span>
<span class="the-footer__console-prompt">&gt;</span> keeper_protocol.init()
<span class="the-footer__console-prompt">&gt;</span> loading manifest...
<span class="the-footer__console-output">STATUS: OPERATIONAL</span>
<span class="the-footer__console-output">NETWORK: MAINNET</span>
<span class="the-footer__console-output">KEEPERS ONLINE: <span id="footerLiveCount">2,847</span></span>
<span class="the-footer__console-prompt">&gt;</span> <span class="the-footer__console-cursor"></span></pre>
        </div>
      </div>

      <!-- Column 2: Discover more -->
      <div class="the-footer__col the-footer__col--discover">
        <h3 class="the-footer__col-heading">DISCOVER MORE</h3>
        <nav class="the-footer__nav" aria-label="Footer navigation">
          <a href="#" class="the-footer__nav-link">STORY</a>
          <a href="#" class="the-footer__nav-link">JOURNAL</a>
          <a href="#" class="the-footer__nav-link">MEDIA</a>
          <a href="#" class="the-footer__nav-link">GALLERY</a>
          <a href="#" class="the-footer__nav-link">ABOUT</a>
          <a href="#" class="the-footer__nav-link the-footer__nav-link--external">CAREERS
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M1 9L9 1M9 1H3M9 1V7" stroke="currentColor" stroke-width="1"/>
            </svg>
          </a>
        </nav>
      </div>

      <!-- Column 3: Social -->
      <div class="the-footer__col the-footer__col--social">
        <h3 class="the-footer__col-heading">JOIN THE CONVERSATION</h3>
        <div class="the-footer__social-links">
          <a href="https://twitter.com/kaboraworld" class="the-footer__social-link" target="_blank" rel="noopener noreferrer" aria-label="Twitter / X">
            {ICON_TWITTER}
            <span>TWITTER</span>
          </a>
          <a href="https://discord.gg/keepers" class="the-footer__social-link" target="_blank" rel="noopener noreferrer" aria-label="Discord">
            {ICON_DISCORD}
            <span>DISCORD</span>
          </a>
        </div>
      </div>

      <!-- Column 4: Contact -->
      <div class="the-footer__col the-footer__col--contact">
        <h3 class="the-footer__col-heading">MORE DETAILS</h3>
        <p class="the-footer__contact-text">CONTACT US AT</p>
        <a href="mailto:hello@kprverse.com" class="the-footer__email">HELLO@KPRVERSE.COM</a>
        <a href="#" class="the-footer__download-btn">
          {ICON_DOWNLOAD}
          <span>DOWNLOAD BRAND BOOK</span>
        </a>
      </div>

    </div>

    <!-- Giant logo -->
    <div class="the-footer__logo-wrap">
      <div class="the-footer__logo-text" aria-hidden="true">
        <svg class="the-footer__logo-svg" viewBox="0 0 1200 160" fill="none" xmlns="http://www.w3.org/2000/svg">
          <text x="0" y="140" font-family="'Inter','ABCWhytePlus',sans-serif" font-weight="900" font-size="160" letter-spacing="-8" fill="currentColor">KEEPERS</text>
        </svg>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="the-footer__bottom">
      <div class="the-footer__bottom-left">
        <div class="the-footer__lang-select">
          <button class="the-footer__lang-btn is-active">EN</button>
          <button class="the-footer__lang-btn">JA</button>
          <button class="the-footer__lang-btn">KR</button>
        </div>
      </div>
      <div class="the-footer__bottom-center">
        <a href="#" class="the-footer__legal-link">PRIVACY POLICY</a>
        <span class="the-footer__legal-sep">&middot;</span>
        <a href="#" class="the-footer__legal-link">TERMS</a>
      </div>
      <div class="the-footer__bottom-right">
        <span class="the-footer__copyright">&copy; 2022 KEEPERS</span>
      </div>
    </div>

  </div>
</footer>
'''


# =========================================================================== #
#  14. Console
# =========================================================================== #

def console_html() -> str:
    """Fixed overlay console panel with terminal UI."""
    return f'''
<!-- ====== CONSOLE ====== -->
<div class="the-console" id="theConsole" aria-hidden="true" role="dialog" aria-label="Console">

  <!-- SVG background shape -->
  <svg class="the-console__bg-shape" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <path d="M0 8C0 3.58 3.58 0 8 0H560L600 40V392C600 396.42 596.42 400 592 400H40L0 360V8Z"
          fill="#0a0e1a" stroke="#8ca6ff" stroke-width="1"/>
  </svg>

  <div class="the-console__inner">

    <!-- Header bar -->
    <div class="the-console__header">
      <div class="the-console__header-left">
        <span class="the-console__header-dot"></span>
        <span class="the-console__header-label">ENCRYPTED PROTOCOL AZ02-37780423</span>
      </div>
      <div class="the-console__header-center">
        <span class="the-console__header-network">KEEP MAINNET</span>
      </div>
      <div class="the-console__header-right">
        <button class="the-console__close js-console-close" id="consoleCloseBtn" aria-label="Close console">
          {ICON_CLOSE}
        </button>
      </div>
    </div>

    <!-- Scrollable output -->
    <div class="the-console__output" id="consoleOutput">
      <p class="the-console__line the-console__line--system">
        <span class="the-console__line-prefix">[SYS]</span> KEEPER PROTOCOL v4.2.1 INITIALIZED
      </p>
      <p class="the-console__line the-console__line--system">
        <span class="the-console__line-prefix">[SYS]</span> SECURE CONNECTION ESTABLISHED
      </p>
      <p class="the-console__line the-console__line--system">
        <span class="the-console__line-prefix">[SYS]</span> WELCOME, KEEPER. TYPE 'HELP' FOR COMMANDS.
      </p>
      <p class="the-console__line the-console__line--info">
        <span class="the-console__line-prefix">[NET]</span> 2,847 KEEPERS ONLINE
      </p>
      <p class="the-console__line the-console__line--info">
        <span class="the-console__line-prefix">[NET]</span> LAST BLOCK: #4,219,037
      </p>
    </div>

    <!-- Command input -->
    <div class="the-console__input-wrap">
      <span class="the-console__input-prompt">&gt;</span>
      <input type="text" class="the-console__input" id="consoleInput"
             placeholder="ENTER COMMAND..." autocomplete="off" spellcheck="false" />
      <span class="the-console__input-cursor"></span>
    </div>

  </div>
</div>
'''


# =========================================================================== #
#  15. Assembler
# =========================================================================== #

def get_all_sections(images: dict) -> str:
    """Assemble every section in page order into a single HTML string."""
    return (
        preloader_html()
        + canvas_container_html()
        + frame_html()
        + nav_mobile_html()
        + menu_html()
        + landing_html(images)
        + project_intro_html(images)
        + project_story_html(images)
        + collection_intro_html(images)
        + collection_gallery_html(images)
        + tableau_sections_html(images)
        + launch_html(images)
        + footer_html()
        + console_html()
    )
