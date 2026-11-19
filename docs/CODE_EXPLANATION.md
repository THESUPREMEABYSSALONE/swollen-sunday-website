# Swollen Sunday 2026 — Code Explanation

**A beginner's guide to the HTML and CSS behind the website**

Written for Level 200 students who have just finished four weeks of HTML and CSS.
Every section of the site is explained in plain English, with analogies, and with
notes on how to change things safely.

---

## 1. How to read this guide

Think of the website as a **house**:

- **HTML** is the building itself — the walls, doors, rooms and furniture. It decides *what is on the page*.
- **CSS** is the paint, the curtains and the lighting. It decides *how everything looks*.
- **JavaScript** is the electricity — it makes things *do* something. This site has almost none, on purpose. Only the contact form uses a script, and that script is supplied by the lecturer.

The website has two pages:

| Page | File | Job |
|---|---|---|
| Home page | `index.html` | The recap story: hero, videos, about, gallery preview, event details, schedule, FAQs, contact form |
| Gallery page | `gallery.html` | All 20 photos and 15 videos in grids |

Both pages share **one** stylesheet: `css/style.css`.

---

## 2. Folder structure

```
swollen-sunday-website/
├── index.html                  the home page
├── gallery.html                the photo and video page
├── css/
│   └── style.css               the only stylesheet
├── js/
│   └── form.js                 the only script (placeholder for the lecturer's code)
├── images/                     30 .jpeg pictures
├── videos/                     16 .mp4 videos
└── docs/                       these study materials
```

**Why this matters:** the folders keep the project tidy. If a file is moved, every
link that points to it breaks. For example, `images/Group pic.jpeg` is written in
HTML as `images/Group%20pic.jpeg`, because a browser cannot read a space in a URL.
`%20` is the code for a space.

---

## 3. The HTML skeleton (every page needs this)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Swollen Sunday 2026 | Recap &amp; Highlights</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  ...
</body>
</html>
```

| Line | What it does | Analogy |
|---|---|---|
| `<!DOCTYPE html>` | Tells the browser "this is HTML5". | Showing your ID at the gate. |
| `<html lang="en">` | The root element. `lang` helps screen readers pronounce words. | The whole building. |
| `<meta charset="UTF-8">` | Lets the page show symbols such as ©, • and é correctly. | Choosing the right alphabet. |
| `<meta name="viewport" ...>` | Makes the page use the phone's real width instead of pretending to be a desktop. **Without this line mobile design fails.** | Asking the builder to measure the actual plot. |
| `<title>` | The words on the browser tab. | The name on the gate. |
| `<link rel="stylesheet">` | Connects the CSS file. | Plugging in the lighting cable. |

### The Google Fonts links

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Google Fonts is allowed because it is not a framework or library — it only supplies
two extra fonts. **Anton** is the tall, bold heading font. **Inter** is the clean
body font. If the internet is slow or offline, the CSS fallbacks
(`Arial Black`, `Segoe UI`) take over automatically.

---

## 4. index.html, section by section

The page is built with **semantic tags** — tags that describe their job:
`header`, `nav`, `main`, `section`, `article`, `figure`, `figcaption`, `footer`.
They look the same as `<div>` on screen but they help screen readers, search
engines and your examiner understand the page.

### Section 1 — Header and navigation

```html
<header class="site-header">
  <div class="nav-wrap">
    <a class="brand" href="#home">
      <span class="brand-mark">SS</span>
      <span class="brand-text">Swollen Sunday <em>2026</em></span>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <a href="#home">Home</a>
      ...
      <a href="gallery.html">Gallery</a>
    </nav>
  </div>
</header>
```

- `<header>` is the top bar.
- `.brand` is a link back to the top. The gold square is a `<span>`, not an image, so it loads instantly.
- `<nav>` holds the six menu links. `aria-label` gives screen readers a name for this block.
- `#home` means "jump to the element with `id="home"` on this page".
- `gallery.html` means "open the other page".
- On `gallery.html` the same links are written `index.html#about`, because the target is on a different page.

**To edit:** change the words inside the `<a>` tags. To add a link, copy one line.
The styling lives in CSS section 4.

### Section 2 — Hero

```html
<section class="hero" id="home">
  <div class="hero-slides" aria-hidden="true">
    <div class="slide slide-1"></div>
    <div class="slide slide-2"></div>
    <div class="slide slide-3"></div>
    <div class="slide slide-4"></div>
  </div>
  <div class="hero-overlay" aria-hidden="true"></div>
  <div class="hero-content">
    <p class="eyebrow light">Post-Event Recap · 15 November 2026</p>
    <h1>Thousands Gathered. Lives Changed Forever.</h1>
    <p class="hero-sub">Relive ...</p>
    <div class="hero-actions">
      <a class="btn btn-primary pulse" href="#recap-videos">Watch the Recap Video</a>
      <a class="btn btn-ghost" href="gallery.html">Browse Photo Gallery</a>
    </div>
  </div>
</section>
```

Three layers, like a theatre stage:

1. `.hero-slides` — four empty `<div>`s at the back. Each one gets a photo from CSS (`background-image`) and they fade into each other.
2. `.hero-overlay` — a dark see-through sheet so white text is readable on any photo.
3. `.hero-content` — the text and buttons, lifted above the other layers with `z-index: 2`.

`aria-hidden="true"` tells screen readers to skip the decorative photo layers.

`<h1>` is used **once** per page: the biggest heading. All later headings are `<h2>` and `<h3>`.

**To edit:** the headline is plain text in the `<h1>`. The four hero photos are set
in CSS (`.slide-1` to `.slide-4`), not in the HTML, so you change them in one place.

### Section 3 — Recap video strip

```html
<section class="recap" id="recap-videos">
  <article class="video-card">
    <video controls preload="metadata">
      <source src="videos/pixelad.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <h3>The Official Invitation</h3>
    <p>The advert that filled the stadium...</p>
  </article>
  ...
</section>
```

- `<video>` is the HTML5 player. `controls` shows play, volume and fullscreen buttons.
- `preload="metadata"` only loads the length and first frame — **not** the whole file. This is why a page with 15 videos still opens quickly.
- `<source>` points to the file. The text inside `<video>` only appears in very old browsers.
- `<article>` is used because each card makes sense on its own.
- `id="recap-videos"` is the target of the hero's first button.

**To edit:** the file name inside `src`, the `<h3>` title and the `<p>` description.

### Section 4 — About the gathering

```html
<section class="about" id="about">
  <div class="container split">
    <div class="about-text">...</div>
    <div class="about-collage">
      <figure class="collage-item tall">
        <img src="images/Entrance.jpeg" alt="...">
        <figcaption>The gates open</figcaption>
      </figure>
      ...
    </div>
  </div>
  <div class="container">
    <div class="highlights">...</div>
  </div>
</section>
```

- `.container` centres content and caps the width at 1180px.
- `.split` is a **CSS Grid** with two columns on desktop, one on phones.
- `<figure>` groups a picture with its caption. `<figcaption>` is the caption text — the correct semantic way to caption an image.
- `.tall` and `.wide` are helper classes that make one collage photo span two rows or two columns.
- The three `.highlight` articles are the emoji points (worship, Word, community). Emoji are just text, so no image files are needed.

**To edit:** text is plain paragraphs. Swap a collage photo by changing its `src`.
Add a fourth highlight by copying one `<article class="highlight">` block.

### Section 5 — Pastors and vision

```html
<section class="pastors" id="pastors">
  <div class="container split pastors-split">
    <article class="video-card dark-card"> ... swollenhistory.mp4 ... </article>
    <div class="pastor-grid">
      <figure class="pastor">
        <img src="images/dag.jpeg" alt="...">
        <figcaption>[EDIT] Host — name and role</figcaption>
      </figure>
      ...
    </div>
  </div>
</section>
```

- The `id="pastors"` is the target of the "Meet Our Pastors & Vision" button.
- Four `<figure class="pastor">` cards hide their `<figcaption>` until you hover — a **CSS-only reveal** (opacity and transform).
- Captions say `[EDIT]` because we must never guess who is in a photograph. Replace them with the real names and roles.

**To edit:** replace each `[EDIT] ...` caption with verified information.

### Section 6 — Gallery preview

```html
<section class="preview">
  <div class="container">
    <div class="head-row">
      <div><p class="eyebrow">Gallery</p><h2 class="section-title">...</h2></div>
      <a class="btn btn-outline" href="gallery.html">See Full Gallery</a>
    </div>
    <div class="photo-grid">
      <a class="photo" href="images/dag.jpeg" target="_blank" rel="noopener">
        <img src="images/dag.jpeg" alt="...">
        <span class="photo-cap">Host portrait</span>
      </a>
      ...
    </div>
  </div>
</section>
```

- Each photo is an `<a>` wrapping an `<img>`, so the whole picture is clickable.
- `href` points at the **full-size image**, `target="_blank"` opens it in a new tab, and `rel="noopener"` is a small security precaution.
- `alt` describes the photo for blind users and for when an image fails to load.
- `.photo-cap` is a caption that slides up on hover.

**To edit:** copy one `<a class="photo">` block and change the three places the file name appears (`href`, `src`, and the caption).

### Section 7 — Event information

```html
<section class="event" id="details">
  <div class="info-grid">
    <article class="info-card">
      <span class="badge">Event Archive</span>
      <h3>Where It Happened</h3>
      <ul class="info-list">
        <li><span class="ico">📅</span><span><strong>Date</strong>Sunday, November 15, 2026</span></li>
        ...
      </ul>
      <a class="text-link" href="https://www.google.com/maps/..." target="_blank">View Stadium Directions &amp; Parking Map →</a>
    </article>
    <article class="info-card next-card"> ... </article>
  </div>
  <div class="map-wrap">
    <iframe title="Map showing the University of Ghana Stadium" src="https://www.google.com/maps?q=...&output=embed" loading="lazy"></iframe>
  </div>
</section>
```

- `<ul class="info-list">` is an unordered list of facts; each `<li>` holds an emoji and a text block.
- `<strong>` makes the small label ("Date", "Time") bold. CSS turns it into a tiny uppercase label.
- The second card has the extra class `next-card`, which paints it navy. One class change, completely different look.
- `<iframe>` embeds the Google Map. `title` describes it for screen readers, `loading="lazy"` waits until the map is near the screen before loading it.
- `&amp;` is how you write a real `&` in HTML.

**To edit:** facts are plain text. The map address lives inside the `src` after `q=`.

### Section 8 — Upcoming schedule

```html
<section class="schedule" id="schedule">
  <article class="schedule-card">
    <div class="date-badge">
      <span class="month">Nov</span>
      <span class="day">22</span>
    </div>
    <div class="schedule-body">
      <h3>Post-Swollen Sunday Thanksgiving Service</h3>
      <ul class="meta">
        <li>🗓️ Sunday, November 22, 2026</li>
        ...
      </ul>
      <p>...</p>
      <div class="card-links">
        <a class="btn btn-small" href="#contact">Plan Your Visit</a>
        <a class="text-link" href="https://calendar.google.com/calendar/render?...">Add to Calendar</a>
      </div>
    </div>
  </article>
  ...
</section>
```

- The date badge is two `<span>`s inside one box. On phone it is a small horizontal pill; on desktop CSS turns it into a tall block (`flex-direction: column`).
- `.meta` is a list of date, time and place.
- The "Add to Calendar" links use Google Calendar's template URL. The date is written in a special format: `20261122T073000Z` means 22 November 2026, 07:30, UTC (Ghana is GMT+0).
- The midweek link adds `recur=RRULE:FREQ=WEEKLY;BYDAY=WE` to repeat every Wednesday.

**To edit:** change the visible words and the matching dates inside the calendar links.
Keep the `T` and the `Z` in the date format.

### Section 9 — FAQ

```html
<section class="faq" id="faq">
  <a class="faq-banner" href="images/faq.jpeg" target="_blank"><img src="images/faq.jpeg" alt="..."></a>
  <div class="faq-row">
    <a class="faq-card" href="images/faq1.jpeg" target="_blank">
      <img src="images/faq1.jpeg" alt="Swollen Sunday FAQ card 1">
    </a>
    ... nine cards ...
  </div>
</section>
```

- The nine cards sit in a **Flexbox row** with `overflow-x: auto`, so they can be swiped sideways on a phone and scrolled with the mouse on a desktop.
- `scroll-snap-type` makes the row stop neatly on each card.
- Each card is a link, so tapping opens the full readable image in a new tab.
- Hovering a card scales the **card**, not the picture, so no text is ever cut off.

**To edit:** to add a question, copy a card and change `faq9` to `faq10` in both places.

**Note on the artwork:** the ten FAQ images were rebuilt in the site's navy and gold style because the supplied posters named "Independence Square" instead of the UG Stadium and gave the start time as 2 PM. The original files are still in `docs/faq-originals/` if the client prefers them. `docs/make_faq_images.py` regenerates the new cards.

### Section 10 — Contact

```html
<section class="contact" id="contact">
  <div class="container split contact-split">
    <div class="contact-info">
      <div class="contact-block">
        <h3>Call or WhatsApp Us</h3>
        <p><a class="phone" href="tel:+233530502572">053 050 2572</a></p>
        <a class="btn btn-whatsapp" href="https://wa.me/233530502572" target="_blank">Chat on WhatsApp</a>
      </div>
      ...
    </div>
    <div class="form-wrap">
      <form id="contact-form" class="contact-form">
        <div class="field">
          <label for="fullname">Full Name</label>
          <input type="text" id="fullname" name="fullname" required>
        </div>
        ...
        <button class="btn btn-primary btn-block" type="submit">Send Message</button>
      </form>
    </div>
  </div>
</section>
```

Form rules that matter:

| Rule | Why |
|---|---|
| Every input has an `id` | So its `<label for="...">` can connect to it. Clicking the label puts the cursor in the box. |
| Every input has a `name` | The script reads the value by this name. `fullname`, `phone`, `topic`, `message`. |
| `type="tel"` | Phones show the number keypad. |
| `required` | The browser refuses to submit an empty field. |
| `<select>` with `<option>`s | The six reasons for contacting the church. |
| `type="submit"` | The button that sends the form. |

`tel:+233530502572` opens the phone dialler. `https://wa.me/233530502572` opens a
WhatsApp chat with that number. Both use the international format, starting `+233`.

### Section 11 — Footer

```html
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col"><h2 class="footer-title">Swollen Sunday 2026</h2><p>...</p></div>
    <div class="footer-col"><h2 class="footer-title">Quick Links</h2><ul class="footer-links">...</ul></div>
    ...
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p>© 2026 Swollen Sunday • First Love Church. All rights reserved.</p>
      <p>Built for the Kingdom • Accra, Ghana.</p>
    </div>
  </div>
</footer>
```

- Four `footer-col` blocks sit in a grid: about, quick links, contact, service times.
- `<h2>` is used (not `<h3>`) so the heading order never skips a level.
- The bottom bar is a separate row with a thin top border.

### Floating WhatsApp button

```html
<a class="whatsapp" href="https://wa.me/233530502572" target="_blank" aria-label="Chat with First Love Church on WhatsApp">
  <span aria-hidden="true">💬</span>
</a>
```

`position: fixed` keeps it in the bottom-right corner while the page scrolls.
`aria-label` gives the button a spoken name because the emoji alone is not descriptive.

---

## 5. gallery.html

The page reuses the same `<header>`, `<nav>`, `<footer>` and WhatsApp button.
Only three things are new:

1. **`.page-head`** — a dark title banner with an `<h1>` ("Every Face. Every Moment.") and a short intro.
2. **Photo grid** — twenty `<a class="photo show">` cards. The extra class `show` keeps the caption visible all the time, which is friendlier on a gallery page.
3. **Video grid** — fifteen `<article class="video-card">` blocks with a `<video>` and a title. Each caption begins with `[EDIT]` so the team can fill in the real description.

There is **no** `<script>` on this page. The home page keeps the only script tag.

**To edit a video caption:** change the `<p>` under the `<h3>`.
**To add a photo:** copy one card, change `src`, `href` and the caption text.

---

## 6. CSS, block by block

`css/style.css` is organised in 19 numbered sections with a comment above every
block. Read the comments in the file — they match this guide.

### 6.1 Section 1 — `:root` variables

```css
:root {
  --primary: #0b1e3d;
  --secondary: #d4a12a;
  --accent: #4fb3e8;
  --light: #f4f7fc;
  --dark: #061225;
}
```

A variable is a **named paint pot**. `var(--secondary)` means "use the gold paint".
Change the hex code in one place and every button, underline and badge changes
with it.

| Variable | Where you see it |
|---|---|
| `--primary` | Navbar, headings, date badges, footer text |
| `--secondary` | Buttons, eyebrows, borders, gold accents |
| `--accent` | Focus rings, small labels on dark backgrounds |
| `--light` | Page background of alternating sections and the form |
| `--dark` | Recap band, footer, hero overlay |

Also stored here: `--radius` (rounded corners), `--shadow` (soft shadow), and the
two font stacks. **This is the first place to edit when the course rep sends the
official colours.**

### 6.2 Section 2 — Reset and base

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
```

- `*` selects every element.
- `box-sizing: border-box` means padding and borders are counted **inside** the width. Without it, a 100% wide box with padding becomes wider than the screen.
- `margin: 0; padding: 0` removes the browser's default gaps so we control spacing ourselves.

```css
html { scroll-behavior: smooth; scroll-padding-top: 170px; }
```

- `scroll-behavior: smooth` makes menu links glide down the page.
- `scroll-padding-top` stops the sticky header from covering the heading you jumped to.

```css
body { font-family: var(--font-body); font-size: 16px; line-height: 1.7; ... }
```

`line-height: 1.7` means 1.7 times the font size between lines — comfortable reading.

```css
img, video { display: block; max-width: 100%; }
```

`display: block` removes the tiny gap browsers leave under pictures.
`max-width: 100%` stops pictures overflowing their container on small screens.

### 6.3 Section 3 — Shared helpers

| Block | Purpose |
|---|---|
| `.container` | Centres content: `max-width: 1180px; margin: 0 auto; padding: 0 20px;` |
| `.eyebrow` | Tiny uppercase gold label above a heading (`letter-spacing: 3px`) |
| `.section-title` | Big `<h2>` size, with a bottom margin |
| `.section-lead` | Short grey intro paragraph, capped at 680px for easy reading |
| `.btn` | The pill-shaped base for every button |
| `.btn:hover` | `transform: translateY(-3px)` — lifts the button |
| `.btn-primary` | Gold button with a soft glow shadow |
| `.pulse` | Attaches the `glow` animation |
| `.btn-ghost` | Transparent button with a white outline for dark photos |
| `.btn-outline` | White button with a navy outline for light sections |
| `.btn-whatsapp` | Green WhatsApp button |
| `.btn-small` | Smaller padding for cards |
| `.btn-block` | `width: 100%` for the form button |
| `.text-link` | Underlined plain link used beside buttons |

### 6.4 Section 4 — Sticky header

```css
.site-header { position: sticky; top: 0; z-index: 50; }
```

- `sticky` with `top: 0` means "scroll normally until you reach the top, then stay there".
- `z-index: 50` keeps the bar above photos and cards.

```css
.nav-wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; }
```

- Flexbox puts the logo and menu on one line.
- `flex-wrap: wrap` lets the menu drop to a second line on a phone instead of squashing.
- On phones `.nav { width: 100% }` makes the links take the whole second row; at 768px `width: auto` puts everything back on one line.

`.nav a` styles each link as a small pill; `:hover` fills it with faint white;
`.active` is the gold pill showing the current page.

### 6.5 Section 5 — Hero and the crossfade

```css
.slide {
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  animation: fadeSlide 24s infinite;
}
.slide-2 { animation-delay: 6s; }
```

- `position: absolute` with all four sides at `0` stretches the div over the whole hero.
- `background-size: cover` fills the area without stretching the photo.
- All four slides start invisible. Each one runs the same 24-second animation, but slides 2, 3 and 4 start 6, 12 and 18 seconds later. The result is a crossfade loop with **no JavaScript**.

`@keyframes fadeSlide` (section 17) fades in over the first 4%, stays visible until
25%, fades out by 30%, and stays hidden for the rest of the cycle. The small
`scale()` changes add a slow zoom.

Hero text uses `@keyframes fadeUp`, with different delays (0.05s, 0.2s, 0.45s,
0.7s) so the eyebrow, headline, paragraph and buttons appear one after another.
`both` in the animation shorthand keeps the final state.

### 6.6 Section 6 — Recap video strip

- `.recap` paints the band dark and adds 70px of space top and bottom.
- `.video-grid` is a **Grid**: one column on phones, two at 768px, three at 1024px.
- `.video-card` is white, rounded, with `box-shadow` and a hover lift.
- `.recap .video-card` overrides that to a glassy see-through card on the dark band.
- `video { height: 200px; object-fit: cover; }` gives every clip the same neat frame regardless of its real shape. `object-fit: cover` crops instead of stretching.

### 6.7 Section 7 — About and collage

```css
.split { display: grid; grid-template-columns: 1fr; gap: 40px; }
```

`1fr` means "one share of the available space". One column on phones. At 1024px a
media query changes it to `1fr 1fr` — two equal columns.

- `.about-collage` is a two-column grid. `.tall` spans two rows; `.wide` spans both columns with `grid-column: span 2`.
- `overflow: hidden` on the framed photo is what makes the zoom stay inside the rounded corners.
- `.highlights` is a grid of three equal cards at 768px and above.

### 6.8 Section 8 — Pastor cards

`.pastor` is the frame. The `<figcaption>` is placed on top with `position: absolute`,
then hidden with `opacity: 0`. On `:hover` it becomes `opacity: 1` and slides up
with `transform: translateY(0)`. The photo zooms at the same time. This is the
classic CSS-only reveal — no script, no checkbox trick.

`linear-gradient(transparent, rgba(6,18,37,0.94))` is the dark fade behind the
caption so white text stays readable over any photo.

### 6.9 Section 9 — Photo grids

- `.photo-grid` starts at one column; 2 columns at 768px; 4 at 1024px.
- `.photo` is the frame (`overflow: hidden`, rounded). `.photo img` has a fixed height and `object-fit: cover`.
- `.photo:hover img { transform: scale(1.08); }` gives the zoom.
- `.photo-cap` is hidden until hover. `.photo.show .photo-cap` keeps it visible on the gallery page.

### 6.10 Section 10 — Event cards

- `.info-grid` is a grid of two cards on desktop.
- `border-top: 4px solid var(--secondary)` draws the gold stripe along the top.
- `.next-card` overrides the background to navy and the text to white.
- `.badge` is the small uppercase pill.
- `.info-list .ico` is a rounded square holding the emoji.
- `.map-wrap { filter: grayscale(1); }` softens the map. `:hover` changes it to `grayscale(0.15)` so the colour fades back in.

### 6.11 Section 11 — Schedule cards

On phones the card is a simple block and the badge is a row. At 1024px:

```css
.schedule-card { display: grid; grid-template-columns: 92px 1fr; }
.date-badge { flex-direction: column; }
```

The badge becomes a 92px column on the left and the text takes the rest.
`align-self: start` stops the badge stretching to the full card height.

### 6.12 Section 12 — FAQ row

```css
.faq-row {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
}
.faq-card {
  flex: 0 0 270px;
  scroll-snap-align: start;
}
```

- `overflow-x: auto` is the whole trick: the row scrolls sideways when the cards are wider than the screen.
- `flex: 0 0 270px` means "never shrink, never grow, stay 270px wide".
- `scroll-snap-align: start` makes each card click into place when you stop swiping.
- `.faq-card:hover { transform: scale(1.03) }` zooms the card itself so the picture inside is never cropped.
- The banner is capped at 420px wide because the artwork is portrait, not landscape.

### 6.13 Section 13 — Contact and form

- `.contact-split` uses a 0.9 / 1.1 split at desktop, giving the form slightly more room.
- `.contact-block` has `border-left: 3px solid var(--secondary)` — the gold rule beside each detail.
- `.field` spaces each label-and-input pair.
- Inputs share one rule so they all look the same.
- The **focus state** is important for accessibility:

```css
.field input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 4px rgba(79, 179, 232, 0.2);
}
```

A sky-blue border plus a soft ring shows keyboard users exactly where they are.

### 6.14 Section 14 — Footer

`background: var(--dark)` with `rgba(255,255,255,0.7)` text. One column on phones,
two at 768px, four at 1024px. `.footer-bottom` adds a thin top border and a
`space-between` row for the two copyright lines.

### 6.15 Section 15 — Floating WhatsApp button

```css
.whatsapp {
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 60;
  width: 56px;
  height: 56px;
  border-radius: 50%;
}
```

`position: fixed` pins it to the screen, not the page. `border-radius: 50%` makes
it a circle. The `greenPulse` animation adds the soft green ring.

### 6.16 Section 16 — Gallery page styles

`.page-head` is the dark title banner. `.gallery-block` is the white section
wrapper, and `.video-block` paints the video section light grey so the two halves
are visually separate. `.photo-grid.four` is the 20-photo grid.

### 6.17 Section 17 — Animations

```css
@keyframes fadeSlide { ... }   /* hero crossfade */
@keyframes fadeUp   { ... }   /* text rising into place */
@keyframes glow     { ... }   /* gold button pulse */
@keyframes greenPulse { ... } /* WhatsApp pulse */
```

Keyframes are a **film script**: `0%` is the start, `100%` is the end. The browser
fills in everything in between.

### 6.18 Sections 18 and 19 — Media queries

```css
@media (min-width: 768px) { ... }   /* tablet */
@media (min-width: 1024px) { ... } /* desktop */
```

The site is built **mobile first**: the plain rules are the phone design, and the
media queries only *add* bigger layouts. That is why there are only two
breakpoints and no `max-width` queries.

What changes at each breakpoint:

| Feature | Phone | 768px | 1024px |
|---|---|---|---|
| Nav | Two wrapped rows | One row | One row |
| About / Pastors / Contact | 1 column | 1 column | 2 columns |
| Photo grid | 1 column | 2 columns | 4 columns |
| Video grid | 1 column | 2 columns | 3 columns |
| Highlights | 1 column | 3 columns | 3 columns |
| Event cards | 1 column | 1 column | 2 columns |
| Schedule | 1 column | 1 column | 2 columns |
| Footer | 1 column | 2 columns | 4 columns |
| Date badge | Small pill | Small pill | Tall block |

---

## 7. Flexbox and Grid — when we use which

**Flexbox is for a line of things.** It works in one direction: a row or a column.

Used for: the navbar, the button rows, the FAQ swipe row, the date badge,
the footer bottom bar.

```css
.hero-actions { display: flex; justify-content: center; gap: 14px; }
```

**Grid is for a layout of things.** It works in two directions at once: rows *and* columns.

Used for: photo grids, video grids, the about split, the schedule, the highlights,
the footer columns.

```css
.photo-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
```

`repeat(4, 1fr)` means "four equal columns". A one-line change turns it into a
three-column grid.

Simple rule of thumb: **one direction → Flexbox. Two directions → Grid.**

---

## 8. The form script (the only JavaScript)

In `index.html`, just before `</body>`:

```html
<script src="js/form.js"></script>
```

`js/form.js` currently contains only a comment. The lecturer will supply the real
script. It will:

1. Listen for the form's `submit` event.
2. Stop the page from reloading (`preventDefault`).
3. Read the values using the `name` attributes: `fullname`, `phone`, `topic`, `message`.
4. Send them somewhere (email service or Google Sheet).
5. Show a thank-you message.

**Why only one script?** The brief is a pure HTML/CSS project. Everything visual —
the slideshow, the hover reveals, the swipe row, the pulsing buttons — is done in
CSS so the site still works if JavaScript is switched off.

**To swap the script:** open `js/form.js`, delete the comment, paste the lecturer's
code, save. Do not add a second `<script>` tag and do not put JavaScript inside the
HTML.

---

## 9. How to change things safely

### Change the colours

Edit the five hex codes at the top of `css/style.css`. Nothing else needs to change.

### Change the fonts

1. Go to fonts.google.com and pick two fonts.
2. Replace the `<link href="...">` line in **both** HTML files.
3. Change `--font-head` and `--font-body` in `:root`.

### Change a photo

Find the `<img src="images/...">` and change the file name. If the new name has a
space, write `%20` instead. Also change `alt` text so it still describes the picture.

### Change a video

Change the `src` of the `<source>` tag. Keep `controls preload="metadata"` —
that is what keeps the page fast.

### Add a schedule card

Copy a whole `<article class="schedule-card">` block and edit the badge, title,
list and Google Calendar link.

### Find every `[EDIT]` placeholder

Search the project for `[EDIT]`. They are in: the four pastor captions, the email
line in Contact, and fifteen gallery video captions.

---

## 10. Testing checklist

Test at **360px** (small phone), **768px** (tablet) and **1280px** (laptop).

- [ ] The page never scrolls sideways.
- [ ] The sticky navbar stays on top and the menu links wrap instead of overlapping.
- [ ] Every photo loads and every video shows a player.
- [ ] All six nav links work on both pages, including `index.html#about` from the gallery.
- [ ] Hovering a photo zooms it; hovering a pastor card reveals the caption.
- [ ] The FAQ row scrolls sideways and snaps.
- [ ] The WhatsApp button stays in the corner while scrolling.
- [ ] The form cannot be submitted empty (the browser blocks it).
- [ ] Keyboard Tab shows a blue ring on each form field.
- [ ] The map loads and is grey until hovered.
- [ ] There is no JavaScript on `gallery.html`, and only `form.js` on `index.html`.

---

## 11. Glossary

| Word | Meaning |
|---|---|
| **Element** | A piece of HTML, such as `<p>` or `<img>`. |
| **Tag** | The label in angle brackets, e.g. `<section>`. |
| **Attribute** | Extra information inside a tag, e.g. `src="..."`, `href="..."`, `alt="..."`. |
| **Selector** | The part of CSS that chooses what to style: `p`, `.card`, `#home`. |
| **Class** | A reusable name, written `.card` in CSS and `class="card"` in HTML. |
| **ID** | A unique name for one element, written `#home`. Used for page jumps. |
| **Property** | What you are changing, e.g. `color`, `padding`, `display`. |
| **Value** | What you set it to, e.g. `navy`, `20px`, `flex`. |
| **Box model** | Content + padding + border + margin — the four layers around every element. |
| **Flexbox** | A one-direction layout system for rows or columns. |
| **Grid** | A two-direction layout system of rows and columns. |
| **Media query** | A rule that only applies at certain screen widths. |
| **Breakpoint** | The width where a media query switches on (768px, 1024px). |
| **Viewport** | The visible area of the browser window. |
| **Semantic HTML** | Tags that describe meaning (`header`, `nav`, `article`) instead of `div`. |
| **`object-fit: cover`** | Fills a box with an image, cropping the overflow instead of stretching. |
| **`var(--primary)`** | Reads the value stored in a CSS variable. |
| **`z-index`** | Which layer sits on top when elements overlap. |
| **Pseudo-class** | A state such as `:hover` or `:focus`. |
| **`@keyframes`** | The script for an animation, from 0% to 100%. |
| **`overflow-x: auto`** | Adds a sideways scrollbar only when needed. |
| **`scroll-snap`** | Makes a scrolling row stop neatly on each item. |
| **Placeholder** | The grey example text inside an empty input. |
| **`alt` text** | A written description of an image for screen readers. |

---

## 12. Common questions an examiner may ask

**1. Why did you use only HTML and CSS?**
The brief required a zero-JavaScript recap site. CSS can already do hover effects,
animations, a slideshow, a swipe row and smooth scrolling, so JavaScript was not
needed. The single script is the contact form, supplied by the lecturer.

**2. How does the hero slideshow work without JavaScript?**
Four absolutely positioned divs share one 24-second `@keyframes` animation. Each
has a different `animation-delay` (0s, 6s, 12s, 18s), so only one is visible at a
time and they fade into each other.

**3. Why is the site "mobile first"?**
The base CSS is the phone design, and the two media queries add columns for larger
screens. This keeps the phone version simple and avoids overriding lots of desktop
rules.

**4. What is the difference between Flexbox and Grid here?**
Flexbox lays out items along one line (navbar, buttons, FAQ row). Grid lays out
rows and columns together (photo grid, schedule, footer).

**5. How do you keep a page with fifteen videos fast?**
Every `<video>` uses `preload="metadata"`, so only the first frame and duration
load. The full file downloads only when the user presses play.

**6. Why `object-fit: cover` on images?**
The photos come in different shapes. `cover` fills the frame neatly and crops the
overflow, so the grid stays even without stretching faces.

**7. Why are there two HTML files instead of one long page?**
The gallery has 20 photos and 15 videos. Splitting it keeps the home page focused
on the story and makes each page load faster and easier to read.

**8. What makes the site accessible?**
Semantic tags, `alt` text on every image, labels tied to inputs with `for`/`id`,
`aria-label` on the WhatsApp button, `title` on the map iframe, a visible focus
ring, and enough colour contrast for text.

**9. Where are the colours defined and why?**
In `:root` as CSS variables. Changing five values re-skins the entire site, which
is useful when the client's real brand colours arrive.

**10. How would you add a tenth FAQ card?**
Copy one `<a class="faq-card">` block, change `faq9` to `faq10` in the `href` and
`src`, and update the `alt` text. The Flexbox row handles the rest automatically.

**11. Why `scroll-padding-top` on `html`?**
The navbar is sticky. Without that padding, jumping to `#schedule` would put the
heading underneath the navbar.

**12. What happens if an image file is missing?**
The `alt` text appears in its place and the layout keeps its shape, because every
image sits in a fixed-height frame.

**13. Why is the form's button `type="submit"`?**
So the browser knows it submits the form and can run the built-in `required`
checks before any script runs.

**14. Can the site work offline?**
Yes, apart from the Google Fonts and the embedded map. The CSS falls back to
Arial Black and Segoe UI if the fonts do not load.

---

*End of guide. Keep this file in `docs/` and read it beside the code.*
