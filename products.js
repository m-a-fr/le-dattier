// ============================================================
// CATALOGUE PRODUITS — LE DATTIER
// ============================================================
// Pour modifier un produit, changer son prix, ou en ajouter un
// nouveau, modifiez ce fichier.
// ============================================================

const products = [

  // ========================
  // 🌴 DATTES
  // ========================
  {
    id: "datte-deglet-nour",
    name: "Deglet Nour Premium",
    origin: "Algérie",
    cat: "dattes",
    emoji: "🌴",
    desc: "La reine des dattes. Texture fondante, notes de miel et de caramel.",
    price: 18.90,
    unit: "500g",
    badge: "best",
    img: "images/prod-deglet.jpg",
    weight: 520
  },
  {
    id: "datte-medjool",
    name: "Medjool Royale",
    origin: "Palestine",
    cat: "dattes",
    emoji: "👑",
    desc: "Charnue et généreuse, aux saveurs de caramel beurré. Un pur délice.",
    price: 24.50,
    unit: "500g",
    badge: "new",
    img: "images/prod-medjool.jpg",
    weight: 520
  },
  {
    id: "datte-ajwa",
    name: "Ajwa de Médine",
    origin: "Arabie Saoudite",
    cat: "dattes",
    emoji: "🕌",
    desc: "La datte sacrée. Saveur intense, légèrement boisée et sucrée.",
    price: 32.00,
    unit: "400g",
    badge: "",
    img: "images/prod-ajwa.jpg",
    weight: 420
  },
  {
    id: "datte-sukari",
    name: "Sukari d'Al-Qassim",
    origin: "Arabie Saoudite",
    cat: "dattes",
    emoji: "✨",
    desc: "Douce et croustillante, au goût de sucre d'orge. Rare et précieuse.",
    price: 28.00,
    unit: "400g",
    badge: "",
    img: "images/prod-sukari.jpg",
    weight: 420
  },
  {
    id: "datte-mazafati",
    name: "Mazafati de Bam",
    origin: "Iran",
    cat: "dattes",
    emoji: "🌙",
    desc: "Moelleuse et juteuse. Un fondant exceptionnel aux notes de chocolat.",
    price: 19.90,
    unit: "500g",
    badge: "",
    img: "images/prod-mazafati.jpg",
    weight: 520
  },
  {
    id: "datte-coffret",
    name: "Coffret Découverte Dattes",
    origin: "Multi-origines",
    cat: "dattes",
    emoji: "🎁",
    desc: "5 variétés d'exception réunies dans un coffret cadeau élégant.",
    price: 45.00,
    unit: "coffret",
    badge: "new",
    img: "images/prod-coffret-dattes.jpg",
    weight: 800
  },

  // ========================
  // 🧼 SAVONS
  // ========================
  {
    id: "savon-alep-laurier",
    name: "Savon d'Alep au Laurier",
    origin: "Syrie",
    cat: "savons",
    emoji: "🫒",
    desc: "40% huile de laurier. Saponifié à froid selon la tradition millénaire d'Alep.",
    price: 12.90,
    unit: "200g",
    badge: "best",
    img: "images/prod-savon-laurier.jpg",
    weight: 220
  },
  {
    id: "savon-nigelle",
    name: "Savon Noir à la Nigelle",
    origin: "Maroc",
    cat: "savons",
    emoji: "🖤",
    desc: "Enrichi en huile de nigelle. Purifiant et nourrissant pour la peau.",
    price: 9.90,
    unit: "150g",
    badge: "",
    img: "images/prod-savon-nigelle.jpg",
    weight: 170
  },
  {
    id: "savon-rose",
    name: "Savon à la Rose de Damas",
    origin: "Turquie",
    cat: "savons",
    emoji: "🌹",
    desc: "À l'eau de rose de Damas. Hydratant et délicatement parfumé.",
    price: 11.50,
    unit: "150g",
    badge: "new",
    img: "images/prod-savon-rose.jpg",
    weight: 170
  },
  {
    id: "savon-olive",
    name: "Savon à l'Huile d'Olive",
    origin: "Palestine",
    cat: "savons",
    emoji: "🌿",
    desc: "100% huile d'olive extra vierge. Le savon ancestral de Naplouse.",
    price: 8.90,
    unit: "120g",
    badge: "",
    img: "images/prod-savon-olive.jpg",
    weight: 140
  },

  // ========================
  // 🏺 HUILE DE NIGELLE
  // ========================
  {
    id: "nigelle-pure",
    name: "Huile de Nigelle Pure",
    origin: "Égypte",
    cat: "nigelle",
    emoji: "🏺",
    desc: "Première pression à froid. Graines de Nigella Sativa d'Égypte.",
    price: 16.90,
    unit: "100ml",
    badge: "best",
    img: "images/prod-nigelle-pure.jpg",
    weight: 150
  },
  {
    id: "nigelle-bio",
    name: "Huile de Nigelle Bio",
    origin: "Éthiopie",
    cat: "nigelle",
    emoji: "🌱",
    desc: "Certifiée bio. Issue de graines éthiopiennes réputées pour leur pureté.",
    price: 22.50,
    unit: "100ml",
    badge: "new",
    img: "images/prod-nigelle-bio.jpg",
    weight: 150
  },
  {
    id: "nigelle-capsules",
    name: "Capsules de Nigelle",
    origin: "Égypte",
    cat: "nigelle",
    emoji: "💊",
    desc: "60 capsules d'huile de nigelle pure. Cure de bien-être quotidienne.",
    price: 18.90,
    unit: "60 caps",
    badge: "",
    img: "images/prod-nigelle-capsules.jpg",
    weight: 100
  },
  {
    id: "nigelle-coffret",
    name: "Coffret Nigelle Prestige",
    origin: "Égypte",
    cat: "nigelle",
    emoji: "🎁",
    desc: "Huile pure 100ml + capsules 60 + savon nigelle. Le rituel complet.",
    price: 39.90,
    unit: "coffret",
    badge: "",
    img: "images/prod-coffret-nigelle.jpg",
    weight: 500
  },
];
