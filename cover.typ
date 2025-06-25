#import "@preview/dashing-dept-news:0.1.1": newsletter, article

#show: newsletter.with(
  title: [Problems Solutions],
  edition: [
    April 2025 \
    Enzo Serenato
  ],
  hero-image: (
    image: image("knot.png"),
    caption: [Modern Operating Systems],
    height: 50%
  ),
  publication-info: [
    Enzo Serenato. \
    Ponta Grossa, Paraná. \
    #link("mailto:enzoserenato@gmail.com")
  ],
)


#quote(block: true, attribution: [Linus Torvalds])[
  Theory and practice sometimes clash. And when that happens, theory loses. Every single time.
]

#article[
  = Capítulos 1 - 2
  Por hora, somente as soluções dos problemas dos capítulos 1 e 2 de _Modern Operating Systems_ de Andrew S. Tanenbaum.
]
