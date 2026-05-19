const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const outDir = path.join(root, "docs", "ruflo_revenue_machine");
const htmlPath = path.join(outDir, "ruflo_revenue_machine.html");
const pdfPath = path.join(outDir, "ruflo_revenue_machine.pdf");
const previewPath = path.join(outDir, "preview_cover.png");
const qaPaths = [
  path.join(outDir, "qa_ranking.png"),
  path.join(outDir, "qa_decision.png"),
  path.join(outDir, "qa_prompts.png"),
];

fs.mkdirSync(outDir, { recursive: true });

const sources = [
  {
    name: "McKinsey - The State of AI 2025",
    url: "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
    note:
      "23% de organizaciones escalando agentes y 39% experimentando; impacto EBIT todavía limitado en muchas empresas.",
  },
  {
    name: "Microsoft Work Trend Index 2025",
    url: "https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born",
    note:
      "81% de líderes espera integrar agentes de forma moderada o extensiva en 12-18 meses.",
  },
  {
    name: "OECD Economic Survey Spain 2025",
    url: "https://www.oecd.org/en/publications/oecd-economic-surveys-spain-2025_abc5c435-en/full-report/fostering-productivity-growth-in-small-and-medium-sized-enterprises_039acae9.html",
    note:
      "Las pymes españolas van por detrás en cloud, big data e IA; solo cerca del 10,4% reporta usar aplicaciones de IA.",
  },
  {
    name: "Banco de España - Adopción de IA en empresas españolas",
    url: "https://www.bde.es/wbe/en/publicaciones/analisis-economico-investigacion/boletin-economico/2025t2-articulo-06-la-adopcion-de-la-inteligencia-artificial-en-las-empresas-espanolas-un-primer-analisis-basado-en-la-ebae.html",
    note:
      "Casi el 20% de firmas encuestadas usan IA; la mayoría sigue experimentando y los obstáculos son talento, coste y datos.",
  },
  {
    name: "Upwork - 2025 Most In-Demand Skills",
    url: "https://www.upwork.com/press/releases/upwork-unveils-2025s-most-in-demand-skills",
    note:
      "Scripting, automation y qualitative research aparecen entre skills crecientes; 49% de empresas usa freelancers para cubrir gaps críticos.",
  },
  {
    name: "Fiverr - Fall 2025 Business Trends Index",
    url: "https://www.fiverr.com/news/2025-fall-business-trends-index/",
    note:
      "Búsquedas de AI automation suben 136%; el mercado premia automatización con criterio humano.",
  },
  {
    name: "Crayon - State of Competitive Intelligence 2025",
    url: "https://www.crayon.co/state-of-competitive-intelligence",
    note:
      "La adopción de IA en competitive intelligence crece 76% interanual; resumir y analizar datos son usos dominantes.",
  },
  {
    name: "HubSpot - 2025 State of Sales",
    url: "https://blog.hubspot.com/sales/hubspot-sales-strategy-report",
    note:
      "Los compradores están más informados; 74% de sales pros cree que la IA facilita la investigación del comprador.",
  },
  {
    name: "Salesforce - State of Sales",
    url: "https://www.salesforce.com/news/stories/sales-ai-statistics-2024/",
    note:
      "Los reps dedican gran parte del tiempo a tareas no comerciales; equipos con IA reportan más crecimiento.",
  },
  {
    name: "6sense - 2025 B2B Buyer Experience",
    url: "https://6sense.com/science-of-b2b/buyer-experience-report-2025/",
    note:
      "La shortlist inicial sigue decidiendo gran parte de las compras B2B; la validación de IA acelera conversaciones.",
  },
  {
    name: "vcita - 2025 SMB Marketing Report",
    url: "https://www.prnewswire.com/news-releases/vcitas-new-survey-of-smb-owners-highlights-marketing-agency-churn-crisis-client-expectations-and-ai-opportunity-302505739.html",
    note:
      "Muchas pymes externalizan marketing, pero abandonan agencias si no ven ROI rápido; oportunidad para entregables de evidencia.",
  },
  {
    name: "BrightLocal - Local Consumer Review Survey 2025",
    url: "https://www.brightlocal.com/research/local-consumer-review-survey-2025/",
    note:
      "Las reviews siguen afectando confianza, visibilidad y decisión; no incentivar reseñas es una regla clave.",
  },
  {
    name: "Adobe Analytics - GenAI traffic to retail sites",
    url: "https://blog.adobe.com/en/publish/2025/03/17/adobe-analytics-traffic-to-us-retail-websites-from-generative-ai-sources-jumps-1200-percent",
    note:
      "El tráfico desde fuentes GenAI a retail crece con fuerza, aunque todavía es canal de investigación y consideración.",
  },
  {
    name: "Adobe - ChatGPT as a search engine",
    url: "https://www.adobe.com/express/learn/blog/chatgpt-as-a-search-engine",
    note:
      "Usuarios y marketers ya tratan ChatGPT como canal de descubrimiento; AI visibility gana importancia.",
  },
  {
    name: "CMS - Data protection and cybersecurity laws in Spain",
    url: "https://cms.law/en/int/expert-guides/cms-expert-guide-to-data-protection-and-cyber-security-laws/spain",
    note:
      "La LSSI española exige consentimiento para comunicaciones comerciales electrónicas salvo soft opt-in.",
  },
  {
    name: "European Commission - Navigating the AI Act",
    url: "https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act",
    note:
      "AI Act aplica en fases: alfabetización IA desde 2025, GPAI desde 2025, aplicación general en 2026.",
  },
];

const opportunities = [
  {
    rank: 1,
    title: "Ruflo Insight Desk para agencias boutique",
    score: 91,
    target:
      "Agencias pequeñas de PR, paid media, SEO, social, branding, product marketing y consultoras boutique que necesitan investigación rápida para clientes.",
    problem:
      "Tienen más demanda de estrategia, reporting y benchmarks que capacidad analítica interna. Si entregan tarde o con poco insight, pierden retención.",
    offer:
      "Servicio white-label de inteligencia en 48 horas: benchmark competitivo, señales de mercado, ángulos de campaña y oportunidades accionables.",
    deliverable:
      "PDF ejecutivo de 12-18 páginas, matriz de competidores, mapa de mensajes, 10 oportunidades tácticas, mini dashboard opcional y briefing para presentar al cliente.",
    price: "Piloto EUR 350-650. Retainer EUR 900-2.000/mes por 3-6 briefs.",
    why:
      "La agencia ya tiene cliente y presupuesto. Compra velocidad, capacidad y mejor percepción estratégica sin contratar analista.",
    ruflo:
      "Investiga sector, extrae señales de demanda, compara competidores, resume reviews/social/search, prepara briefing y genera borrador de presentación.",
    codex:
      "Generador de informes, dashboard reutilizable, scraper ligero de fuentes públicas, landing white-label y plantillas en HTML/PDF.",
    approve:
      "Selección de fuentes, claims estratégicos, precio final, envío al cliente, cualquier insight sensible o recomendación fuerte.",
    tech: "Media-baja",
    commercial: "Media",
    saturation: "Media-baja",
    monthly: "EUR 2.000-6.000 en 60 días; EUR 8.000-15.000 si escala a 8-10 agencias.",
  },
  {
    rank: 2,
    title: "Competitive Intelligence Sprint para B2B SaaS y servicios",
    score: 88,
    target:
      "Startups SaaS seed/Serie A, consultoras B2B, bootstrapped SaaS y empresas de servicios que compiten en mercados ruidosos.",
    problem:
      "No saben explicar por qué elegirlos, qué dicen sus competidores, qué objeciones aparecen ni qué huecos hay en la categoría.",
    offer:
      "Sprint de 5 días para convertir ruido competitivo en battlecard, mapa de posicionamiento y acciones de GTM.",
    deliverable:
      "Battlecard, matriz de posicionamiento, análisis de páginas/pricing/reviews, objeciones frecuentes, recomendaciones de web/copy y demo de dashboard.",
    price: "EUR 750-1.500 por sprint. Retainer EUR 1.000-2.500/mes para monitorización.",
    why:
      "Ayuda a ventas, marketing y founders a ganar claridad rápidamente sin comprar una suite enterprise de CI.",
    ruflo:
      "Detecta competidores, recolecta claims, pricing público, reseñas, menciones, contenido SEO y señales de hiring/funding.",
    codex:
      "Dashboard de competitor tracking, scoring de diferenciación, exportador de battlecards y alertas simples.",
    approve:
      "Lista final de competidores, lectura estratégica, recomendaciones públicas y envío de informe.",
    tech: "Media",
    commercial: "Media",
    saturation: "Media",
    monthly: "EUR 3.000-8.000 inicial; EUR 10.000+ si hay 4-5 retainers.",
  },
  {
    rank: 3,
    title: "Tender/RFP Radar para consultoras pequeñas",
    score: 84,
    target:
      "Consultoras IT, sostenibilidad, ingeniería, marketing público, formación, ciberseguridad y transformación digital de 5-50 personas.",
    problem:
      "Pierden oportunidades por no revisar portales, no tener bid/no-bid rápido o no poder redactar primeras respuestas a tiempo.",
    offer:
      "Radar semanal de licitaciones/RFPs con scoring de encaje y primer borrador de respuesta para oportunidades aprobadas.",
    deliverable:
      "Lista priorizada, matriz bid/no-bid, resumen de requisitos, calendario de deadlines, compliance checklist y borrador inicial.",
    price: "EUR 500 setup + EUR 300-900/mes. Por bid: EUR 400-1.200 según complejidad.",
    why:
      "Un contrato ganado compensa muchos meses. Ahorra horas de búsqueda y evita deadlines perdidos.",
    ruflo:
      "Monitoriza fuentes, clasifica oportunidades, extrae requisitos, prepara matrices y redacta borradores con material del cliente.",
    codex:
      "Bot de scraping/monitoring de portales públicos, base de datos, alertas, generador de matrices y plantillas DOCX/PDF.",
    approve:
      "Bid/no-bid final, claims técnicos, condiciones legales, propuesta enviada y cualquier dato financiero.",
    tech: "Media-alta",
    commercial: "Media-alta",
    saturation: "Media",
    monthly: "EUR 2.000-7.000 inicial; alto upside si un nicho responde.",
  },
  {
    rank: 4,
    title: "Review Mining y Voz del Cliente para conversión",
    score: 82,
    target:
      "Clínicas, dental, estética, hospitality, academias, ecommerce, apps y marcas DTC con reviews públicas y fricción de conversión.",
    problem:
      "Tienen feedback en Google, Trustpilot, Amazon, App Store o redes, pero nadie lo convierte en mejoras de web, oferta y experiencia.",
    offer:
      "Auditoría de reviews y fricción comercial: qué duele, qué convence, qué responder y qué cambiar en copy/servicio.",
    deliverable:
      "Informe visual con temas, sentimiento, frases reales, riesgos reputacionales, quick wins, respuestas sugeridas y roadmap de conversión.",
    price: "EUR 350-900 por auditoría. EUR 300-800/mes para monitorización.",
    why:
      "Se conecta a ingresos y reputación. El cliente ve evidencia directa de su mercado, no opinión genérica.",
    ruflo:
      "Extrae reviews, agrupa temas, detecta quejas repetidas, redacta respuestas y transforma VOC en mejoras de landing/oferta.",
    codex:
      "Crawler de reviews públicas, clasificador, dashboard de temas y generador de reportes recurrentes.",
    approve:
      "Uso de citas, recomendaciones reputacionales, respuestas públicas y cualquier diagnóstico delicado.",
    tech: "Media",
    commercial: "Media",
    saturation: "Media-alta",
    monthly: "EUR 1.500-5.000 inicial; EUR 7.000+ con vertical claro.",
  },
  {
    rank: 5,
    title: "AI Search Visibility & Trust Audit",
    score: 78,
    target:
      "B2B SaaS, ecommerce, hoteles, clínicas premium, formación y marcas que dependen de descubrimiento online.",
    problem:
      "No saben cómo aparecen en ChatGPT, Perplexity, Gemini, AI Overviews ni qué fuentes influyen en sus respuestas.",
    offer:
      "Auditoría de presencia en buscadores IA: queries, menciones, competidores citados, gaps de autoridad y plan de contenido/PR.",
    deliverable:
      "Scorecard AI visibility, matriz de prompts, capturas, fuentes citadas, gaps de entidad, plan de páginas y brief de contenidos.",
    price: "EUR 500-1.200 por auditoría. EUR 700-2.000/mes para tracking y mejoras.",
    why:
      "Es una preocupación emergente; los compradores ya investigan con IA. Se vende como diagnóstico, no como promesa SEO milagrosa.",
    ruflo:
      "Ejecuta prompts controlados, compara respuestas, clasifica fuentes, detecta gaps y redacta plan de autoridad.",
    codex:
      "Runner de prompts, dashboard de respuestas, diff histórico y generador de reportes con capturas.",
    approve:
      "Claims sobre ranking/visibilidad, recomendaciones SEO/PR y cualquier promesa de resultados.",
    tech: "Media",
    commercial: "Media",
    saturation: "Alta emergente",
    monthly: "EUR 2.000-6.000; más si se combina con CI y contenido.",
  },
  {
    rank: 6,
    title: "DTC/Ecommerce Category Intelligence Dashboard",
    score: 76,
    target:
      "Marcas DTC, tiendas Shopify, vendedores marketplace, distribuidores nicho y ecommerce managers.",
    problem:
      "Vigilan competidores manualmente: precios, bundles, reviews, claims, campañas, disponibilidad y cambios de producto.",
    offer:
      "Dashboard mensual de categoría con alertas de pricing, mensajes, reviews y oportunidades de producto/contenido.",
    deliverable:
      "Dashboard, PDF mensual, tracker de cambios, matriz de precios, temas de reviews y recomendaciones de oferta.",
    price: "EUR 600-1.500 setup + EUR 400-1.200/mes.",
    why:
      "Permite reaccionar a competidores y detectar oportunidades de producto con datos visibles.",
    ruflo:
      "Define competidores, monitoriza páginas, reviews y contenido, detecta cambios y prepara narrativa ejecutiva.",
    codex:
      "Scrapers, base de datos, visualización, alertas, scoring de cambios y exportador PDF.",
    approve:
      "Fuentes permitidas, términos de uso, conclusiones comerciales y acciones recomendadas.",
    tech: "Media-alta",
    commercial: "Media",
    saturation: "Media",
    monthly: "EUR 2.000-8.000 según vertical y retención.",
  },
  {
    rank: 7,
    title: "Account Research Packs para founder-led sales",
    score: 74,
    target:
      "Founders B2B, SDR freelancers, consultores y equipos pequeños que hacen outbound de alto valor.",
    problem:
      "Pierden horas investigando cuentas y acaban enviando mensajes genéricos que dañan reputación.",
    offer:
      "Pack semanal de 20-50 cuentas con señal, hipótesis de dolor, angle personalizado y mensaje revisado.",
    deliverable:
      "CSV/CRM con leads puntuados, señal concreta, primera línea personalizada, email/DM, follow-up y motivo de encaje.",
    price: "EUR 300-800/semana o EUR 20-60 por cuenta investigada.",
    why:
      "Aumenta calidad de outreach sin contratar SDR o usar automatización masiva.",
    ruflo:
      "Busca leads, valida fit, encuentra señales, redacta mensajes, prepara cadencias y actualiza CRM.",
    codex:
      "CRM simple, enriquecimiento desde fuentes públicas, deduplicación, scoring y generador de mensajes.",
    approve:
      "Lista final, mensajes antes de envío, límites de frecuencia, canales y exclusiones.",
    tech: "Media-baja",
    commercial: "Media",
    saturation: "Alta",
    monthly: "EUR 1.500-5.000; mejor como complemento de otra oferta.",
  },
  {
    rank: 8,
    title: "AI Workflow Audit con prototipo para pymes españolas",
    score: 72,
    target:
      "Pymes de servicios profesionales, formación, inmobiliaria B2B, asesorías, despachos y operaciones internas de 10-80 empleados.",
    problem:
      "Saben que deberían usar IA, pero no saben dónde tiene ROI, qué automatizar o cómo hacerlo sin riesgo.",
    offer:
      "Diagnóstico de 10 procesos + prototipo funcional de una automatización segura en 10 días.",
    deliverable:
      "Mapa de procesos, matriz ROI/riesgo, SOP, prototipo en Make/n8n/scripts, documentación y plan de adopción.",
    price: "EUR 900-2.500 por sprint. Retainer EUR 500-1.500/mes para mejora.",
    why:
      "La adopción de IA en pymes españolas sigue baja; necesitan acompañamiento práctico, no charla.",
    ruflo:
      "Entrevista, mapea procesos, prioriza automatizaciones, redacta SOPs y genera documentación.",
    codex:
      "Prototipos, scripts, dashboards, formularios, conectores y QA técnico.",
    approve:
      "Acceso a datos, procesos a automatizar, riesgos legales y entrega al cliente.",
    tech: "Media-alta",
    commercial: "Alta",
    saturation: "Alta",
    monthly: "EUR 2.000-7.000 si se consigue confianza; ciclo más lento.",
  },
  {
    rank: 9,
    title: "Market Briefing Subscription para inversores y compradores",
    score: 69,
    target:
      "Search funds, micro-PE, M&A boutiques, fondos pequeños, family offices y compradores de negocios nicho.",
    problem:
      "Necesitan entender mercados pequeños rápido: tamaño, players, señales de crecimiento, riesgos, canales y multiples aproximados.",
    offer:
      "Briefs mensuales de sectores nicho con mapa competitivo, señales de demanda y oportunidades de adquisición.",
    deliverable:
      "Brief PDF, mapa de players, base de datos, señales de growth, riesgos y shortlist de empresas.",
    price: "EUR 1.000-3.000 por deep dive. EUR 1.500-5.000/mes subscription.",
    why:
      "El comprador paga por velocidad y cobertura; el valor de una buena tesis es alto.",
    ruflo:
      "Escanea sectores, recopila empresas, señales financieras públicas, jobs, tráfico, reviews y narrativa estratégica.",
    codex:
      "Base de datos, scoring, visualizaciones, export PDF, pipeline de sectores.",
    approve:
      "Supuestos, estimaciones, advertencias, cualquier dato no verificado y envío.",
    tech: "Media",
    commercial: "Alta",
    saturation: "Media-baja",
    monthly: "EUR 2.000-10.000, pero requiere credibilidad y red.",
  },
  {
    rank: 10,
    title: "Career Intelligence OS para coaches y candidatos",
    score: 64,
    target:
      "Career coaches, bootcamps, juniors tech/marketing, MBAs y candidatos que buscan roles competitivos.",
    problem:
      "La búsqueda de empleo es manual: detectar empresas, adaptar CV, preparar entrevistas y tracking consume horas.",
    offer:
      "Sistema de búsqueda inteligente: target companies, fit scoring, CV tailoring, prep de entrevistas y CRM de oportunidades.",
    deliverable:
      "Dashboard, lista de empresas, matriz de roles, CV/LinkedIn suggestions, cover notes y calendario de seguimiento.",
    price: "EUR 99-250 B2C. EUR 500-1.500 B2B para coaches/bootcamps.",
    why:
      "Tiene demanda y encaja con tu perfil, pero el ACV directo es bajo y exige volumen o partners.",
    ruflo:
      "Investiga ofertas, empresas, señales de contratación, adapta materiales y prepara entrevistas.",
    codex:
      "Job tracker, scoring, dashboard, generador de packs y plantilla Notion/Sheets.",
    approve:
      "Material final del candidato, mensajes a empresas y cualquier afirmación sobre experiencia.",
    tech: "Media-baja",
    commercial: "Media-alta",
    saturation: "Alta",
    monthly: "EUR 500-3.000 inicial; mejor como producto de portfolio o B2B2C.",
  },
];

const agentPrompts = [
  {
    name: "1. Agente de investigación de mercado",
    prompt: `Rol: eres un analista de mercado junior-senior, escéptico y accionable. Tu objetivo es encontrar nichos donde un operador con agentes IA pueda vender entregables en 30-60 días.
Inputs: perfil de Juanma, restricciones, fuentes permitidas, país/idioma, lista inicial de sectores.
Proceso:
1. Explora 8-12 nichos por ciclo.
2. Busca señales de demanda: contratación, dolor público, presupuestos, herramientas caras, foros, reviews, cambios regulatorios, contenido de competidores.
3. Detecta tareas repetitivas que consumen tiempo y se puedan transformar en entregable.
4. Evalúa saturación: número de agencias, herramientas SaaS, facilidad de copiar, ruido de LinkedIn.
Output:
- Nicho
- Cliente objetivo
- Dolor observable
- Evidencia con fuente
- Trabajo manual que Ruflo podría ahorrar
- Entregable posible
- Riesgos
- Hipótesis de precio
Reglas: no inventes datos. Separa evidencia, inferencia y opinión. Si no hay señal de pago, márcalo como débil.`,
  },
  {
    name: "2. Agente de oportunidad",
    prompt: `Rol: eres un comité de inversión operativo. Tu trabajo es matar ideas mediocres antes de que consuman tiempo.
Inputs: oportunidades del agente de investigación.
Scorea 0-5:
- Rapidez para facturar
- Encaje con Juanma
- Porcentaje ejecutable por Ruflo
- Capacidad de Codex para construir activo
- Urgencia del dolor
- Ticket inicial
- Facilidad de encontrar leads
- Riesgo legal/reputacional inverso
- Saturación inversa
Output:
- Ranking
- Razón para priorizar
- Razón para descartar o aparcar
- Experimento mínimo de validación
- Métrica de éxito en 7 días
Reglas: penaliza ideas que dependan de audiencia grande, spam, promesas vagas o implementación enterprise.`,
  },
  {
    name: "3. Agente de oferta",
    prompt: `Rol: eres product marketer y closer ético. Convierte una oportunidad en una oferta concreta que alguien pueda comprar.
Inputs: oportunidad priorizada, segmento, evidencia, restricciones.
Define:
- Nombre de la oferta
- Cliente exacto
- Dolor que reconoce
- Promesa sobria
- Entregables incluidos
- Qué NO incluye
- Precio piloto, precio estándar y retainer
- Garantía segura
- Plazo
- Prerrequisitos del cliente
- Preguntas de discovery
Reglas: no prometas ingresos garantizados, rankings, leads ni automatización sin revisión humana. La oferta debe ser vendible en una llamada de 15 minutos.`,
  },
  {
    name: "4. Agente de producto/entregable",
    prompt: `Rol: eres product manager de entregables de servicios. Diseña un producto operativo, repetible y bonito.
Inputs: oferta aprobada, ejemplos, fuentes, stack disponible: Ruflo + Codex + Sheets/Notion/PDF/HTML.
Output:
- Estructura exacta del entregable
- Plantillas necesarias
- Datos de entrada
- Proceso de producción paso a paso
- Qué automatizar
- Qué revisar manualmente
- Checklist de calidad
- Qué puede construir Codex esta semana
Reglas: el entregable debe poder producirse en menos de 6 horas tras el primer piloto y mejorar con cada cliente.`,
  },
  {
    name: "5. Agente de leads",
    prompt: `Rol: eres researcher comercial, no spammer. Encuentra cuentas con alta probabilidad de valorar la oferta.
Inputs: ICP, geografía, criterios negativos, canales permitidos, límites legales.
Proceso:
1. Define queries de búsqueda y fuentes.
2. Crea lista de cuentas, no solo contactos.
3. Añade señal concreta: cliente ganado, campaña reciente, hiring, cambio web, mala review, nueva vertical, contenido sobre IA, etc.
4. Puntúa fit 0-100.
5. Propón el canal más seguro: intro, LinkedIn, formulario, evento, marketplace, email con consentimiento o soft opt-in.
Output CSV:
Cuenta, URL, segmento, señal, dolor probable, contacto sugerido, canal, fit score, razón, riesgo, próximo paso.
Reglas: no uses datos personales privados. Respeta opt-outs y no-contact.`,
  },
  {
    name: "6. Agente de comunicación",
    prompt: `Rol: eres copywriter B2B sobrio. Escribes como una persona que ha hecho sus deberes.
Inputs: lead aprobado, señal, oferta, tono, canal.
Output:
- Email corto
- LinkedIn DM
- Follow-up 1
- Follow-up 2
- Respuesta si interesa
- Respuesta si no
Reglas:
- Máximo 90 palabras por primer mensaje.
- Una sola idea.
- Personalización conectada al dolor.
- CTA de interés, no reunión de 30 minutos.
- Sin hype de IA.
- Sin "espero que estés bien", sin plantillas obvias.
- Incluye salida elegante si no encaja.`,
  },
  {
    name: "7. Agente de ventas/CRM",
    prompt: `Rol: eres revenue ops assistant. Tu objetivo es que ninguna conversación se pierda.
Inputs: CRM, mensajes, respuestas, estado actual.
Tareas:
- Actualiza estado.
- Resume conversación.
- Propón siguiente acción.
- Redacta respuesta.
- Marca bloqueos.
- Señala oportunidades de upsell.
- Prepara briefing antes de llamada.
Estados: Research, Approved, Drafted, Contacted, Replied, Discovery, Proposal, Won, Lost, Nurture, Do Not Contact.
Reglas: no envíes nada sin aprobación de Juanma. Si hay objeción legal, reputacional o de precio, eleva al agente crítico.`,
  },
  {
    name: "8. Agente crítico",
    prompt: `Rol: eres auditor legal, reputacional, ético y comercial. Tu trabajo es frenar daño antes de que ocurra.
Inputs: oferta, lead list, mensajes, entregables, claims y fuentes.
Revisa:
- ¿Hay spam o automatización irresponsable?
- ¿La promesa es exagerada?
- ¿Se usan datos personales innecesarios?
- ¿Se respetan LSSI/GDPR/ePrivacy y opt-out?
- ¿Hay scraping contra términos de uso?
- ¿Puede dañar la reputación de Juanma?
- ¿Hay riesgo de entregar análisis falso o no verificable?
Output:
- Aprobado / Aprobado con cambios / Bloqueado
- Riesgo
- Cambio exacto recomendado
- Política a añadir
Reglas: si dudas, baja intensidad, pide consentimiento o usa canal más seguro.`,
  },
];

const crmFields = [
  "Account ID",
  "Empresa",
  "URL",
  "Segmento",
  "País",
  "Tamaño",
  "Señal detectada",
  "Dolor probable",
  "Oferta sugerida",
  "Fit score",
  "Contacto público",
  "Canal permitido",
  "Estado",
  "Último touch",
  "Siguiente acción",
  "Fecha siguiente",
  "Respuesta",
  "Objeción",
  "Valor estimado",
  "Aprobación Juanma",
  "Riesgo",
  "Opt-out / no-contact",
];

const outreach = {
  email: {
    subject: "benchmark rápido",
    body: `Hola {{Nombre}},

He estado revisando cómo agencias boutique están usando investigación rápida para justificar mejor estrategia y reporting frente a clientes.

Vi {{señal concreta}} en {{empresa}} y creo que podríais convertirlo en un brief competitivo útil para {{tipo de cliente}} sin cargar al equipo.

Estoy probando un formato white-label de 48h: benchmark + oportunidades + argumentos para cliente. Si te interesa, te mando un ejemplo de 1 página.

Si no encaja, lo dejo aquí.`,
  },
  linkedin: `Hola {{Nombre}}, vi {{señal concreta}} de {{empresa}} y me pareció que encaja con algo que estoy montando: briefs white-label de inteligencia competitiva para agencias pequeñas que necesitan más capacidad estratégica sin contratar analista. ¿Te puedo pasar un ejemplo de 1 página?`,
  follow1: `Hola {{Nombre}}, cierro el círculo.

La idea no es vender "IA", sino quitar trabajo pesado de research: competidores, mensajes, reviews, señales de demanda y oportunidades presentables para cliente.

Si te sirve, puedo hacer un mini diagnóstico de una categoría vuestra y me dices si tiene utilidad real.`,
  follow2: `Último mensaje, {{Nombre}}.

Si ahora no es prioridad, cero problema. ¿Te parece que vuelva a escribir cuando tenga 2-3 ejemplos de briefs white-label más maduros para agencias?`,
  interest: `Genial, gracias.

Para no hacerte perder tiempo: te propongo mandarte un ejemplo corto y, si tiene sentido, hacemos una llamada de 15 minutos. Para adaptarlo, dime solo:
1. ¿Qué tipo de cliente os pide más investigación o estrategia?
2. ¿Qué entregable os consume más tiempo?
3. ¿Preferís formato PDF, deck o dashboard?`,
  no: `Gracias por responder, de verdad.

Lo dejo aquí y no insisto. Si más adelante necesitáis research puntual, benchmarks o briefs para cliente, encantado de ayudar sin compromiso.`,
};

const css = `
@page { size: A4; margin: 13mm; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #17202a;
  background: #f7f4ee;
  line-height: 1.45;
}
.page {
  min-height: 270mm;
  page-break-after: always;
  background: #fffdf8;
  padding: 28px;
  border: 1px solid #e9dfcf;
  position: relative;
  overflow: hidden;
}
.page:last-child { page-break-after: auto; }
.cover {
  background:
    linear-gradient(135deg, rgba(8,72,81,.96), rgba(8,72,81,.82)),
    radial-gradient(circle at 85% 12%, #f4b860 0 16%, transparent 17%),
    #084851;
  color: #fffdf8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.cover:before {
  content: "";
  position: absolute;
  right: -64px;
  bottom: -64px;
  width: 360px;
  height: 360px;
  border: 34px solid rgba(244,184,96,.34);
  border-radius: 50%;
}
.eyebrow {
  text-transform: uppercase;
  letter-spacing: .12em;
  font-size: 10px;
  font-weight: 800;
  color: #d26a5c;
}
.cover .eyebrow { color: #f4b860; }
h1, h2, h3 { margin: 0; line-height: 1.05; letter-spacing: 0; }
h1 { font-size: 56px; max-width: 760px; }
h2 { font-size: 30px; color: #084851; margin-bottom: 14px; }
h3 { font-size: 17px; color: #084851; margin-bottom: 8px; }
p { margin: 0 0 10px; }
.subtitle { font-size: 18px; max-width: 720px; color: rgba(255,253,248,.86); }
.meta { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px; }
.pill {
  border: 1px solid rgba(255,255,255,.28);
  border-radius: 999px;
  padding: 7px 10px;
  font-size: 11px;
  font-weight: 700;
}
.section-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  font-size: 11px;
  text-transform: uppercase;
  color: #d26a5c;
  letter-spacing: .08em;
  margin-bottom: 10px;
}
.grid { display: grid; gap: 12px; }
.two { grid-template-columns: 1fr 1fr; }
.three { grid-template-columns: repeat(3, 1fr); }
.four { grid-template-columns: repeat(4, 1fr); }
.card {
  background: #fffaf0;
  border: 1px solid #eadcc8;
  border-radius: 8px;
  padding: 14px;
}
.dark-card {
  background: #083f47;
  color: #fffdf8;
  border-color: #083f47;
}
.accent-card {
  background: #fff2d5;
  border-color: #f4c982;
}
.metric {
  font-size: 34px;
  font-weight: 900;
  color: #084851;
  margin-bottom: 4px;
}
.dark-card .metric { color: #f4b860; }
.small { font-size: 10.5px; color: #637076; }
.body-small { font-size: 11.8px; }
.body { font-size: 12.6px; }
.lead { font-size: 15px; color: #34444b; max-width: 760px; margin-bottom: 18px; }
.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 10.4px;
  overflow: hidden;
  border: 1px solid #e5d7c3;
  border-radius: 8px;
}
.table th {
  background: #084851;
  color: #fffdf8;
  text-align: left;
  padding: 8px;
  vertical-align: top;
  font-weight: 800;
}
.table td {
  padding: 8px;
  vertical-align: top;
  border-top: 1px solid #eee2d2;
  background: #fffdf8;
}
.table tr:nth-child(even) td { background: #fff8eb; }
.score {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 24px;
  border-radius: 6px;
  background: #d26a5c;
  color: #fff;
  font-weight: 900;
}
.rank {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #084851;
  color: #f4b860;
  font-weight: 900;
}
.opp-title { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.opp-title h3 { margin: 0; font-size: 20px; }
.opp-grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 12px; }
.field {
  border-left: 4px solid #f4b860;
  padding-left: 10px;
  margin-bottom: 8px;
  font-size: 11.5px;
}
.field b { color: #084851; }
.tagrow { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.tag {
  background: #edf3f1;
  color: #084851;
  border: 1px solid #d7e5df;
  border-radius: 999px;
  padding: 4px 7px;
  font-size: 9.5px;
  font-weight: 800;
}
.timeline {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  margin-top: 12px;
}
.step {
  background: #fffaf0;
  border: 1px solid #eadcc8;
  border-top: 5px solid #084851;
  border-radius: 8px;
  padding: 10px;
  font-size: 10.6px;
}
.step strong { color: #084851; display: block; margin-bottom: 5px; }
.flow {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin: 14px 0;
}
.flow .box {
  background: #084851;
  color: #fffdf8;
  border-radius: 8px;
  padding: 12px;
  min-height: 76px;
}
.box b { color: #f4b860; display: block; margin-bottom: 4px; }
.checklist { columns: 2; column-gap: 24px; }
.checklist li { break-inside: avoid; margin-bottom: 6px; }
ul { margin: 0 0 10px 18px; padding: 0; }
li { margin-bottom: 4px; }
.quote {
  border-left: 5px solid #d26a5c;
  background: #fff2d5;
  padding: 12px 14px;
  border-radius: 0 8px 8px 0;
  font-size: 13px;
}
.prompt {
  white-space: pre-wrap;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 8.8px;
  line-height: 1.35;
  background: #0e2930;
  color: #f8efe0;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #174b55;
}
.message {
  white-space: pre-wrap;
  background: #fffaf0;
  border: 1px solid #eadcc8;
  border-radius: 8px;
  padding: 12px;
  font-size: 11px;
}
.source-list li { font-size: 9.8px; margin-bottom: 7px; }
.footer {
  position: absolute;
  left: 28px;
  right: 28px;
  bottom: 14px;
  display: flex;
  justify-content: space-between;
  color: #8a8f8f;
  font-size: 9px;
}
.mini-bar {
  height: 8px;
  background: #e8decf;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 5px;
}
.mini-bar span {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #d26a5c, #f4b860);
}
.decision {
  display: grid;
  grid-template-columns: 1.2fr .8fr;
  gap: 14px;
  align-items: stretch;
}
.big-number {
  font-size: 72px;
  line-height: .9;
  font-weight: 950;
  color: #f4b860;
}
.avoid { background: #fff1ef; border-color: #efb1a8; }
.safe { background: #eef7f2; border-color: #badcc8; }
code {
  background: #f2eadc;
  border: 1px solid #e2d1bb;
  padding: 1px 4px;
  border-radius: 4px;
}
a { color: #084851; text-decoration: none; }
@media print {
  body { background: #fff; }
  .page { border: 0; min-height: 271mm; }
}
`;

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function footer(label) {
  return `<div class="footer"><span>Ruflo Revenue Machine</span><span>${label}</span></div>`;
}

function sourceLinks() {
  return sources
    .map((s) => `<li><a href="${s.url}">${esc(s.name)}</a>: ${esc(s.note)}</li>`)
    .join("");
}

function opportunityCard(o) {
  return `
  <div class="page">
    <div class="opp-title">
      <span class="rank">${o.rank}</span>
      <div>
        <div class="eyebrow">Oportunidad priorizada</div>
        <h2>${esc(o.title)}</h2>
      </div>
      <span style="margin-left:auto" class="score">${o.score}</span>
    </div>
    <div class="opp-grid">
      <div class="card">
        <div class="field"><b>Cliente objetivo:</b> ${esc(o.target)}</div>
        <div class="field"><b>Problema:</b> ${esc(o.problem)}</div>
        <div class="field"><b>Oferta vendible:</b> ${esc(o.offer)}</div>
        <div class="field"><b>Entregable concreto:</b> ${esc(o.deliverable)}</div>
        <div class="field"><b>Precio inicial:</b> ${esc(o.price)}</div>
        <div class="field"><b>Por qué alguien pagaría:</b> ${esc(o.why)}</div>
      </div>
      <div class="grid">
        <div class="card accent-card">
          <h3>Cómo Ruflo ejecuta el 80%</h3>
          <p class="body-small">${esc(o.ruflo)}</p>
        </div>
        <div class="card">
          <h3>Qué haría Codex</h3>
          <p class="body-small">${esc(o.codex)}</p>
        </div>
        <div class="card">
          <h3>Tu aprobación</h3>
          <p class="body-small">${esc(o.approve)}</p>
        </div>
      </div>
    </div>
    <div class="grid four" style="margin-top:12px">
      <div class="card"><b>Dificultad técnica</b><div class="tagrow"><span class="tag">${esc(o.tech)}</span></div></div>
      <div class="card"><b>Dificultad comercial</b><div class="tagrow"><span class="tag">${esc(o.commercial)}</span></div></div>
      <div class="card"><b>Riesgo saturación</b><div class="tagrow"><span class="tag">${esc(o.saturation)}</span></div></div>
      <div class="card dark-card"><b>Potencial mensual</b><p class="body-small" style="margin-top:6px">${esc(o.monthly)}</p></div>
    </div>
    ${footer(`Oportunidad ${o.rank}/10`)}
  </div>`;
}

function promptPage(item, idx) {
  return `
  <div class="card">
    <h3>${esc(item.name)}</h3>
    <div class="prompt">${esc(item.prompt)}</div>
  </div>`;
}

const oppRows = opportunities
  .map(
    (o) => `
      <tr>
        <td><b>${o.rank}</b></td>
        <td><b>${esc(o.title)}</b><br><span class="small">${esc(o.target)}</span></td>
        <td><span class="score">${o.score}</span></td>
        <td>${esc(o.price)}</td>
        <td>${esc(o.tech)}</td>
        <td>${esc(o.commercial)}</td>
        <td>${esc(o.saturation)}</td>
      </tr>`
  )
  .join("");

const crmRows = crmFields
  .map(
    (f, i) => `<tr><td>${i + 1}</td><td><b>${esc(f)}</b></td><td>${esc(
      {
        "Account ID": "Clave única, por ejemplo AG-001.",
        Empresa: "Nombre de cuenta, no solo persona.",
        URL: "Web o perfil público.",
        Segmento: "Agencia SEO, PR, SaaS, consultora, ecommerce, etc.",
        País: "Útil para cumplimiento legal y tono.",
        Tamaño: "Empleados aproximados o rango.",
        "Señal detectada": "Evento concreto que justifica contacto.",
        "Dolor probable": "Hipótesis, no afirmación.",
        "Oferta sugerida": "Insight Desk, CI Sprint, RFP Radar, etc.",
        "Fit score": "0-100 según ICP, señal y capacidad de pago.",
        "Contacto público": "Contacto profesional público o canal corporativo.",
        "Canal permitido": "Intro, LinkedIn, formulario, marketplace, email consentido.",
        Estado: "Research, Approved, Drafted, Contacted, Replied, Discovery, Proposal, Won, Lost, Nurture, Do Not Contact.",
        "Último touch": "Fecha y canal.",
        "Siguiente acción": "Acción concreta y breve.",
        "Fecha siguiente": "Nunca dejar vacío si no está cerrado.",
        Respuesta: "Resumen literal o clasificación.",
        Objeción: "Precio, timing, confianza, no prioridad, legal.",
        "Valor estimado": "Ticket esperado.",
        "Aprobación Juanma": "Sí/No antes de enviar o entregar.",
        Riesgo: "Legal, reputacional, datos, spam, promesa.",
        "Opt-out / no-contact": "Marcar y respetar siempre.",
      }[f] || ""
    )}</td></tr>`
  )
  .join("");

const html = `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Ruflo Revenue Machine</title>
<style>${css}</style>
</head>
<body>
  <section class="page cover">
    <div>
      <div class="eyebrow">Investigación operativa profunda</div>
      <h1>Ruflo Revenue Machine</h1>
      <p class="subtitle">Un sistema de generación de ingresos donde Juanma decide y valida, mientras Ruflo opera investigación, ofertas, leads, comunicación, CRM, entrega y mejora continua.</p>
      <div class="meta">
        <span class="pill">Juan Manuel Muriel Mora</span>
        <span class="pill">Mayo 2026</span>
        <span class="pill">Objetivo: ingresos en 30-60 días</span>
        <span class="pill">LEGO Resale Intelligence = portfolio, no monetización LEGO</span>
      </div>
    </div>
    <div class="grid three" style="position:relative; z-index:1">
      <div class="card dark-card"><div class="metric">10</div><p>oportunidades priorizadas</p></div>
      <div class="card dark-card"><div class="metric">8</div><p>agentes operativos Ruflo</p></div>
      <div class="card dark-card"><div class="metric">30</div><p>días para validar la primera máquina</p></div>
    </div>
  </section>

  <section class="page">
    <div class="section-label">Tesis central</div>
    <h2>No vendas IA. Vende capacidad operativa empaquetada.</h2>
    <p class="lead">La oportunidad real no está en decir "soy una agencia IA", sino en convertir Ruflo en una unidad de operaciones que produzca entregables que ya tienen presupuesto: inteligencia competitiva, research comercial, auditorías de demanda, RFP/tenders, review mining, AI visibility y sistemas internos.</p>
    <div class="grid three">
      <div class="card">
        <div class="metric">23% + 39%</div>
        <p class="body">McKinsey encuentra organizaciones escalando agentes y muchas más experimentando. Hay adopción, pero todavía falta traducción a workflows útiles.</p>
      </div>
      <div class="card">
        <div class="metric">81%</div>
        <p class="body">Microsoft reporta que líderes esperan integrar agentes en su estrategia de IA en 12-18 meses. El cambio organizativo ya tiene lenguaje ejecutivo.</p>
      </div>
      <div class="card">
        <div class="metric">10,4%</div>
        <p class="body">OECD estima bajo uso de IA en pymes españolas. La brecha crea espacio para ofertas prácticas, no consultoría abstracta.</p>
      </div>
    </div>
    <div class="quote" style="margin-top:16px"><b>Decisión estratégica:</b> empezar por servicios productizados de inteligencia y ventas asistidas, porque combinan tu credibilidad actual, alta ejecución por agentes y entregables que Codex puede convertir en activos reutilizables.</div>
    ${footer("Resumen ejecutivo")}
  </section>

  <section class="page">
    <div class="section-label">Lectura del mercado</div>
    <h2>Donde hay dinero real para un equipo de agentes</h2>
    <div class="grid two">
      <div class="card">
        <h3>1. Las empresas compran resultados, no workflows</h3>
        <p class="body-small">El mercado está saturado de herramientas. Lo que falta es alguien que convierta datos dispersos en decisiones, propuestas, mensajes y entregables listos para usar. Por eso las ofertas deben ser "brief", "dashboard", "radar", "sprint" o "pack", no "automatización IA".</p>
      </div>
      <div class="card">
        <h3>2. La brecha está en pymes y equipos pequeños</h3>
        <p class="body-small">Grandes empresas compran suites. Pymes, agencias y startups necesitan capacidad bajo demanda. Pagan si el output es concreto, rápido, verificable y reduce horas reales.</p>
      </div>
      <div class="card">
        <h3>3. El buyer B2B llega más informado</h3>
        <p class="body-small">6sense y HubSpot apuntan a compradores que investigan antes de hablar con ventas. Esto sube el valor de inteligencia competitiva, posicionamiento, confianza y señales de categoría.</p>
      </div>
      <div class="card">
        <h3>4. La seguridad comercial importa</h3>
        <p class="body-small">En España, la LSSI es estricta con comunicaciones comerciales electrónicas. La máquina debe priorizar canales con consentimiento, LinkedIn de baja intensidad, warm intros, formularios y contenido útil.</p>
      </div>
    </div>
    <div class="flow">
      <div class="box"><b>Investigación</b>nichos, dolores, señales, fuentes</div>
      <div class="box"><b>Oferta</b>promesa sobria, precio, límites</div>
      <div class="box"><b>Distribución</b>leads, mensajes, follow-up, CRM</div>
      <div class="box"><b>Entrega</b>PDF, dashboard, propuesta, mejora</div>
    </div>
    <p class="small">Fuentes clave: McKinsey, Microsoft, OECD, Banco de España, Upwork, Fiverr, Crayon, HubSpot, 6sense, Salesforce, Adobe, BrightLocal y CMS.</p>
    ${footer("Lectura de mercado")}
  </section>

  <section class="page">
    <div class="section-label">Ranking</div>
    <h2>Top 10 oportunidades para Ruflo como centro de operaciones</h2>
    <p class="lead">El scoring prioriza rapidez para facturar, encaje con Juanma, capacidad de Ruflo para ejecutar el 80%, capacidad de Codex para crear activos técnicos, dificultad comercial y riesgo reputacional.</p>
    <table class="table">
      <thead><tr><th>#</th><th>Oportunidad</th><th>Score</th><th>Precio inicial</th><th>Técnica</th><th>Comercial</th><th>Saturación</th></tr></thead>
      <tbody>${oppRows}</tbody>
    </table>
    <div class="grid two" style="margin-top:14px">
      <div class="card safe">
        <h3>Mejores para empezar</h3>
        <ul class="body-small">
          <li>Insight Desk para agencias boutique.</li>
          <li>Competitive Intelligence Sprint para B2B.</li>
          <li>Review Mining si se elige un vertical con reviews abundantes.</li>
        </ul>
      </div>
      <div class="card avoid">
        <h3>Aparcar de momento</h3>
        <ul class="body-small">
          <li>AI workflow audit generalista: demasiado competido si no hay nicho.</li>
          <li>Career OS directo a candidatos: ticket bajo y requiere volumen.</li>
          <li>AI visibility solo: venderlo como complemento, no como promesa aislada.</li>
        </ul>
      </div>
    </div>
    ${footer("Top 10")}
  </section>

  ${opportunities.map(opportunityCard).join("")}

  <section class="page">
    <div class="section-label">Elección recomendada</div>
    <h2>La mejor máquina para los próximos 30 días</h2>
    <div class="decision">
      <div class="card dark-card">
        <div class="big-number">#1</div>
        <h3 style="color:#fffdf8">Ruflo Insight Desk para agencias boutique</h3>
        <p class="body">Es la mejor primera apuesta porque vende capacidad a empresas que ya venden servicios, ya tienen clientes, ya entienden el valor de research y pueden comprar un piloto sin comité largo. Además, tu perfil de insights y competitive intelligence encaja de forma natural sin parecer oportunista.</p>
      </div>
      <div class="card accent-card">
        <h3>Oferta inicial</h3>
        <p class="body-small"><b>Nombre:</b> 48h Client Intelligence Brief.</p>
        <p class="body-small"><b>Precio piloto:</b> EUR 450.</p>
        <p class="body-small"><b>Entrega:</b> PDF visual + mini dashboard + 10 oportunidades presentables al cliente.</p>
        <p class="body-small"><b>Upsell:</b> 3 briefs/mes por EUR 1.200.</p>
        <p class="body-small"><b>Garantía:</b> si el brief no es presentable internamente, se rehace una vez sin coste.</p>
      </div>
    </div>
    <div class="grid three" style="margin-top:14px">
      <div class="card"><h3>Por qué ahora</h3><p class="body-small">Agencias sufren presión de ROI y churn; necesitan diferenciarse con insights rápidos sin añadir headcount.</p></div>
      <div class="card"><h3>Por qué tú</h3><p class="body-small">Puedes hablar desde research, social listening, estrategia y portfolio técnico. No suena a "AI bro".</p></div>
      <div class="card"><h3>Por qué Ruflo</h3><p class="body-small">El trabajo es modular: research, síntesis, scoring, drafts, follow-up y QA. Ideal para agentes con revisión humana.</p></div>
    </div>
    ${footer("Decisión")}
  </section>

  <section class="page">
    <div class="section-label">Sistema operativo completo</div>
    <h2>De señal de mercado a ingreso cerrado</h2>
    <div class="flow">
      <div class="box"><b>1. Research</b>Ruflo detecta nichos, fuentes, competidores, dolores y señales de pago.</div>
      <div class="box"><b>2. Validación</b>Agente de oportunidad puntúa y agente crítico bloquea humo.</div>
      <div class="box"><b>3. Oferta</b>Agente de oferta define promesa, scope, precio, garantía y límites.</div>
      <div class="box"><b>4. Activo</b>Codex crea landing, PDF sample, dashboard y plantillas.</div>
      <div class="box"><b>5. Leads</b>Ruflo genera cuentas con señal y canal seguro.</div>
      <div class="box"><b>6. Comunicación</b>Mensajes personalizados, low-friction, aprobados por Juanma.</div>
      <div class="box"><b>7. Seguimiento</b>CRM, próximos pasos, objeciones y propuestas.</div>
      <div class="box"><b>8. Entrega</b>Brief + QA + debrief + mejora de plantilla.</div>
    </div>
    <div class="grid two">
      <div class="card">
        <h3>Qué hace Ruflo automáticamente</h3>
        <ul class="body-small">
          <li>Crear shortlist de nichos y leads con fuentes.</li>
          <li>Preparar research packs y borradores de oferta.</li>
          <li>Redactar mensajes y follow-ups para aprobación.</li>
          <li>Actualizar CRM y detectar conversaciones estancadas.</li>
          <li>Generar primer borrador de entregables.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Qué aprueba Juanma</h3>
        <ul class="body-small">
          <li>Oferta final, precio y promesa.</li>
          <li>Lista de cuentas antes de contacto.</li>
          <li>Cualquier mensaje comercial antes de enviarse.</li>
          <li>Entregables antes de cliente.</li>
          <li>Uso de datos, fuentes delicadas y claims.</li>
        </ul>
      </div>
    </div>
    ${footer("Sistema operativo")}
  </section>

  <section class="page">
    <div class="section-label">Máquina de adquisición y entrega</div>
    <h2>El loop semanal que debe repetirse</h2>
    <div class="timeline">
      <div class="step"><strong>Lunes</strong>Research de 3 nichos, 30 cuentas, señales y dolor. Agente crítico filtra riesgos.</div>
      <div class="step"><strong>Martes</strong>Crear 1 oferta, 1 sample y 1 landing/documento comercial. Juanma aprueba.</div>
      <div class="step"><strong>Miércoles</strong>Contactar 10-15 cuentas por canales seguros. Todo mensaje revisado.</div>
      <div class="step"><strong>Jueves</strong>Follow-up, respuestas, discovery notes, propuestas cortas.</div>
      <div class="step"><strong>Viernes</strong>Entrega de pilotos, QA, debrief, ask de testimonio o referral.</div>
      <div class="step"><strong>Domingo</strong>Revisión de métricas: respuestas, llamadas, wins, objeciones, cambios de oferta.</div>
    </div>
    <div class="grid three" style="margin-top:16px">
      <div class="card"><h3>Métrica de semana 1</h3><p class="body-small">50 cuentas investigadas, 20 aprobadas, 10 contactos seguros, 2 conversaciones, 1 piloto propuesto.</p></div>
      <div class="card"><h3>Métrica de semana 2</h3><p class="body-small">2-3 llamadas, 1 piloto pagado o carta de intención, primera versión de plantilla repetible.</p></div>
      <div class="card"><h3>Métrica de mes 1</h3><p class="body-small">2-4 pilotos, 1 retainer pequeño, 1 caso de ejemplo y sistema de producción reducido a 4-6 horas.</p></div>
    </div>
    ${footer("Loop semanal")}
  </section>

  <section class="page">
    <div class="section-label">Plan exacto</div>
    <h2>Día 1, Día 2, Día 3, Semana 1, Semana 2, Primer mes</h2>
    <div class="grid two">
      <div class="card">
        <h3>Día 1</h3>
        <ul class="body-small">
          <li>Elegir oferta: 48h Client Intelligence Brief.</li>
          <li>Definir ICP inicial: agencias boutique de Madrid/España 5-40 personas.</li>
          <li>Codex crea landing simple y plantilla de PDF sample.</li>
          <li>Ruflo crea 40 cuentas con señal real.</li>
          <li>Juanma aprueba 15 cuentas para contacto.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Día 2</h3>
        <ul class="body-small">
          <li>Crear sample ficticio/anónimo de 3 páginas.</li>
          <li>Ruflo redacta 15 mensajes personalizados.</li>
          <li>Agente crítico revisa LSSI/GDPR, tono y reputación.</li>
          <li>Juanma envía 5-8 contactos de forma manual o semi-manual por LinkedIn/intro/formulario.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Día 3</h3>
        <ul class="body-small">
          <li>Enviar segundo bloque de contactos.</li>
          <li>Preparar respuesta a interés y mini propuesta.</li>
          <li>Crear estructura de discovery de 15 minutos.</li>
          <li>CRM queda vivo con siguiente acción en cada cuenta.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Semana 1</h3>
        <ul class="body-small">
          <li>50 cuentas investigadas.</li>
          <li>20 mensajes aprobados.</li>
          <li>10-15 contactos seguros.</li>
          <li>2 conversaciones reales.</li>
          <li>1 piloto ofrecido a EUR 450.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Semana 2</h3>
        <ul class="body-small">
          <li>Entregar primer piloto o sample ampliado.</li>
          <li>Reducir proceso de producción a plantilla.</li>
          <li>Ajustar oferta según objeciones.</li>
          <li>Probar segundo segmento: agencias SEO/product marketing o consultoras B2B.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Primer mes</h3>
        <ul class="body-small">
          <li>2-4 pilotos vendidos.</li>
          <li>1 retainer de EUR 900-1.200.</li>
          <li>20 leads nuevos/semana.</li>
          <li>1 caso de estudio anónimo.</li>
          <li>Dashboard + generador PDF funcional con Codex.</li>
        </ul>
      </div>
    </div>
    ${footer("Plan 30 días")}
  </section>

  <section class="page">
    <div class="section-label">Primera campaña</div>
    <h2>Campaña piloto para conseguir los primeros clientes</h2>
    <div class="grid two">
      <div class="card accent-card">
        <h3>Segmento</h3>
        <p class="body-small">Agencias boutique de Madrid, Valencia, Barcelona y remoto España que vendan estrategia, paid media, SEO, social, PR, branding o product marketing a B2B/SaaS/servicios.</p>
        <h3>Hipótesis</h3>
        <p class="body-small">Necesitan research para parecer más estratégicas, defender propuestas, retener clientes y diferenciarse, pero no tienen analista dedicado.</p>
      </div>
      <div class="card">
        <h3>Criterios de leads</h3>
        <ul class="body-small">
          <li>5-40 empleados.</li>
          <li>Clientes visibles o case studies.</li>
          <li>Contenido reciente sobre estrategia, research, IA, performance o categoría.</li>
          <li>No ser agencia masiva ni solo social posting.</li>
          <li>Señal clara para personalizar.</li>
        </ul>
      </div>
    </div>
    <div class="grid three" style="margin-top:14px">
      <div class="card"><h3>Oferta</h3><p class="body-small">"Te preparo un brief competitivo white-label en 48h para una categoría o cliente vuestro. Si no es presentable internamente, lo rehago una vez."</p></div>
      <div class="card"><h3>Prueba</h3><p class="body-small">Portfolio técnico LEGO como evidencia de que sabes construir dashboards e informes, aclarando que no monetizas LEGO.</p></div>
      <div class="card"><h3>CTA</h3><p class="body-small">No pedir llamada al inicio. Pedir permiso para enviar ejemplo de 1 página.</p></div>
    </div>
    <div class="quote" style="margin-top:14px"><b>Regla de campaña:</b> 10-15 contactos por semana, todos con señal real y revisión manual. Mejor 8 mensajes buenos que 100 malos.</div>
    ${footer("Campaña piloto")}
  </section>

  <section class="page">
    <div class="section-label">CRM simple</div>
    <h2>Plantilla de CRM para Ruflo + Juanma</h2>
    <p class="lead">Puede vivir en Google Sheets, Airtable, Notion o SQLite. Lo importante es que cada lead tenga señal, estado, siguiente acción y control de permisos.</p>
    <table class="table">
      <thead><tr><th>#</th><th>Campo</th><th>Uso</th></tr></thead>
      <tbody>${crmRows}</tbody>
    </table>
    ${footer("CRM")}
  </section>

  <section class="page">
    <div class="section-label">Mensajes reales</div>
    <h2>Outreach seguro y con baja fricción</h2>
    <div class="grid two">
      <div class="card">
        <h3>Email frío</h3>
        <p class="small">Usar solo tras revisión legal/canal permitido. En España, priorizar consentimiento, soft opt-in, formulario o LinkedIn.</p>
        <div class="message">Asunto: ${esc(outreach.email.subject)}

${esc(outreach.email.body)}</div>
      </div>
      <div class="card">
        <h3>LinkedIn DM</h3>
        <div class="message">${esc(outreach.linkedin)}</div>
      </div>
      <div class="card">
        <h3>Follow-up 1</h3>
        <div class="message">${esc(outreach.follow1)}</div>
      </div>
      <div class="card">
        <h3>Follow-up 2</h3>
        <div class="message">${esc(outreach.follow2)}</div>
      </div>
    </div>
    ${footer("Mensajes 1/2")}
  </section>

  <section class="page">
    <div class="section-label">Mensajes reales</div>
    <h2>Respuestas según interés</h2>
    <div class="grid two">
      <div class="card safe">
        <h3>Si muestran interés</h3>
        <div class="message">${esc(outreach.interest)}</div>
      </div>
      <div class="card avoid">
        <h3>Si dicen que no</h3>
        <div class="message">${esc(outreach.no)}</div>
      </div>
    </div>
    <div class="card" style="margin-top:16px">
      <h3>Discovery de 15 minutos</h3>
      <ul class="body-small checklist">
        <li>¿Qué cliente o categoría os consume más research ahora?</li>
        <li>¿Qué entregable repetís y os quita tiempo?</li>
        <li>¿Qué señales os gustaría tener antes de una propuesta?</li>
        <li>¿Qué formato presentaríais internamente: PDF, deck, dashboard?</li>
        <li>¿Qué nivel de profundidad sería suficiente para pagar un piloto?</li>
        <li>¿Qué no debería tocar o prometer el brief?</li>
      </ul>
    </div>
    ${footer("Mensajes 2/2")}
  </section>

  <section class="page">
    <div class="section-label">Reglas de seguridad</div>
    <h2>Cómo evitar spam, promesas falsas y daño reputacional</h2>
    <div class="grid two">
      <div class="card safe">
        <h3>Ruflo puede hacer solo</h3>
        <ul class="body-small">
          <li>Investigar cuentas y fuentes públicas.</li>
          <li>Crear borradores de mensajes, ofertas y entregables.</li>
          <li>Puntuar leads y oportunidades.</li>
          <li>Actualizar CRM.</li>
          <li>Proponer próximos pasos.</li>
          <li>Preparar QA checklist.</li>
        </ul>
      </div>
      <div class="card avoid">
        <h3>Requiere aprobación de Juanma</h3>
        <ul class="body-small">
          <li>Enviar cualquier mensaje comercial.</li>
          <li>Usar emails o datos personales.</li>
          <li>Prometer resultados, ROI, rankings o ventas.</li>
          <li>Publicar, entregar o reenviar informes.</li>
          <li>Scrapear sitios con términos restrictivos.</li>
          <li>Responder objeciones delicadas.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Cuándo parar</h3>
        <ul class="body-small">
          <li>Si alguien pide no ser contactado.</li>
          <li>Si no hay señal real que justifique contacto.</li>
          <li>Si la oferta exige datos sensibles.</li>
          <li>Si el cliente espera garantías de ingresos.</li>
          <li>Si el análisis depende de fuentes no verificadas.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Anti-spam operativo</h3>
        <ul class="body-small">
          <li>Máximo 10-15 contactos/semana al inicio.</li>
          <li>Cada mensaje debe tener una señal individual.</li>
          <li>No usar secuencias automáticas masivas.</li>
          <li>No insistir más de 2 follow-ups.</li>
          <li>Registrar opt-out y no-contact.</li>
        </ul>
      </div>
    </div>
    <div class="quote" style="margin-top:14px"><b>Nota legal:</b> esto no sustituye asesoramiento jurídico. En España, la LSSI trata el email comercial con opt-in salvo excepciones como soft opt-in. La vía más segura para empezar es permiso, warm intro, LinkedIn manual, formularios corporativos y marketplaces.</div>
    ${footer("Seguridad")}
  </section>

  <section class="page">
    <div class="section-label">Prompts Ruflo</div>
    <h2>Prompts específicos para cada agente</h2>
    <div class="grid two">
      ${agentPrompts.slice(0, 4).map(promptPage).join("")}
    </div>
    ${footer("Prompts 1/2")}
  </section>

  <section class="page">
    <div class="section-label">Prompts Ruflo</div>
    <h2>Prompts específicos para cada agente</h2>
    <div class="grid two">
      ${agentPrompts.slice(4).map(promptPage).join("")}
    </div>
    ${footer("Prompts 2/2")}
  </section>

  <section class="page">
    <div class="section-label">Codex build plan</div>
    <h2>Qué debe construir Codex para hacer la máquina repetible</h2>
    <div class="grid two">
      <div class="card">
        <h3>Activos técnicos de semana 1</h3>
        <ul class="body-small">
          <li>Landing local o web simple: oferta, ejemplo, CTA.</li>
          <li>Plantilla HTML/PDF del Client Intelligence Brief.</li>
          <li>CRM en CSV/SQLite con estados y scoring.</li>
          <li>Script de generación de reportes desde JSON.</li>
          <li>Plantilla de sample anónimo.</li>
        </ul>
      </div>
      <div class="card">
        <h3>Activos técnicos de mes 1</h3>
        <ul class="body-small">
          <li>Dashboard de competidores y señales.</li>
          <li>Extractor de fuentes públicas permitidas.</li>
          <li>Generador de battlecards.</li>
          <li>Prompt runner para AI visibility controlado.</li>
          <li>QA automático de claims: fuente, fecha, confianza, riesgo.</li>
        </ul>
      </div>
      <div class="card accent-card">
        <h3>Primer MVP exacto</h3>
        <p class="body-small">Un generador de brief que reciba: cliente, sector, competidores, fuentes, señales, hipótesis y output deseado. Devuelve PDF con resumen ejecutivo, matriz competitiva, mensajes, oportunidades y próximos pasos.</p>
      </div>
      <div class="card dark-card">
        <h3 style="color:#fffdf8">Principio</h3>
        <p class="body-small">Codex no debe construir una plataforma antes de vender. Debe construir plantillas y automatizaciones que reduzcan la segunda entrega a la mitad.</p>
      </div>
    </div>
    ${footer("Codex")}
  </section>

  <section class="page">
    <div class="section-label">Decisión final</div>
    <h2>Si solo construyes una máquina en 30 días</h2>
    <div class="card dark-card">
      <h3 style="color:#fffdf8">Construye Ruflo Insight Desk para agencias boutique.</h3>
      <p class="body">Porque une tus capacidades actuales con una necesidad real y comprable: agencias y consultoras pequeñas necesitan research, benchmarks e inteligencia para vender y retener clientes, pero no quieren contratar a tiempo completo. Ruflo puede producir el 80% del trabajo y Codex puede convertir cada entrega en sistema reutilizable.</p>
    </div>
    <div class="grid three" style="margin-top:14px">
      <div class="card">
        <h3>Primer paso hoy</h3>
        <p class="body-small">Crea una landing/documento de una página con la oferta "48h Client Intelligence Brief" y un sample anónimo de 3 páginas.</p>
      </div>
      <div class="card">
        <h3>Primer KPI</h3>
        <p class="body-small">Conseguir 2 respuestas reales de agencias en 7 días. No optimices nada antes de hablar con mercado.</p>
      </div>
      <div class="card">
        <h3>Primer ingreso</h3>
        <p class="body-small">Vender 1 piloto a EUR 450. Después convertirlo en retainer de 3 briefs/mes.</p>
      </div>
    </div>
    <div class="quote" style="margin-top:16px">Tu ventaja no es tener "agentes". Es dirigirlos con criterio de research, empaquetar outputs que alguien pueda comprar y mantener revisión humana donde importa.</div>
    ${footer("Decisión final")}
  </section>

  <section class="page">
    <div class="section-label">Fuentes</div>
    <h2>Fuentes usadas y señales de investigación</h2>
    <p class="lead">Estas fuentes se usaron como evidencia de mercado. Las oportunidades combinan evidencia externa con inferencia operativa sobre qué puede ejecutar Ruflo y qué puede construir Codex.</p>
    <ul class="source-list">${sourceLinks()}</ul>
    ${footer("Fuentes")}
  </section>
</body>
</html>`;

fs.writeFileSync(htmlPath, html, "utf8");

(async () => {
  const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  const launchOptions = fs.existsSync(chromePath)
    ? { headless: true, executablePath: chromePath }
    : { headless: true };
  const browser = await chromium.launch(launchOptions);
  const page = await browser.newPage({ viewport: { width: 1240, height: 1754 }, deviceScaleFactor: 1 });
  await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle" });
  await page.screenshot({ path: previewPath, fullPage: false });
  const qaIndexes = [3, 15, 23];
  for (let i = 0; i < qaIndexes.length; i += 1) {
    const locator = page.locator(".page").nth(qaIndexes[i]);
    await locator.screenshot({ path: qaPaths[i] });
  }
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
  });
  await browser.close();
  console.log(JSON.stringify({ htmlPath, pdfPath, previewPath, qaPaths }, null, 2));
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
