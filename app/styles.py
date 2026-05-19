import streamlit as st


def apply_global_styles() -> None:
    """Aplica la direccion visual premium de Fase 3."""
    st.markdown(
        """
        <style>
        :root {
            --lri-bg: #f4f1ea;
            --lri-surface: #fffdf8;
            --lri-surface-2: #f9f6ee;
            --lri-ink: #171717;
            --lri-muted: #6f6a61;
            --lri-line: rgba(23, 23, 23, 0.12);
            --lri-red: #b91c1c;
            --lri-yellow: #d6a900;
            --lri-green: #116b4f;
            --lri-black: #111111;
            --lri-shadow: 0 18px 45px rgba(23, 23, 23, 0.08);
        }

        *,
        *:before,
        *:after {
            box-sizing: border-box;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                linear-gradient(180deg, rgba(255,255,255,0.74), rgba(244,241,234,0.94)),
                repeating-linear-gradient(
                    90deg,
                    rgba(17,17,17,0.025) 0,
                    rgba(17,17,17,0.025) 1px,
                    transparent 1px,
                    transparent 84px
                ),
                var(--lri-bg);
            color: var(--lri-ink);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.1rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, span, label, div {
            letter-spacing: 0;
        }

        .lri-topline {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            margin-bottom: 22px;
            color: var(--lri-muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }

        .lri-mark {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            color: var(--lri-ink);
        }

        .lri-mark-logo {
            width: 34px;
            height: 34px;
            border-radius: 5px;
            object-fit: cover;
            box-shadow: 0 10px 24px rgba(185,28,28,0.22);
        }

        .lri-nav-wrap {
            position: sticky;
            top: 0.6rem;
            z-index: 10;
            margin-bottom: 26px;
        }

        .lri-nav-wrap [data-baseweb="tab-list"] {
            gap: 8px;
            border: 1px solid var(--lri-line);
            border-radius: 999px;
            background: rgba(255,253,248,0.78);
            box-shadow: 0 16px 34px rgba(23,23,23,0.08);
            backdrop-filter: blur(18px);
            padding: 6px;
        }

        .lri-nav-wrap [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 8px 18px;
            min-height: 38px;
            color: var(--lri-muted);
            font-weight: 800;
            letter-spacing: 0.02em;
        }

        .lri-nav-wrap [aria-selected="true"] {
            background: #111111;
            color: #fffdf8;
        }

        .lri-nav-wrap [data-baseweb="tab-highlight"] {
            display: none;
        }

        .lri-hero {
            display: grid;
            grid-template-columns: minmax(0, 1.35fr) minmax(260px, 0.65fr);
            gap: 28px;
            align-items: stretch;
            margin-bottom: 26px;
        }

        .lri-hero-copy {
            border-top: 1px solid var(--lri-line);
            padding-top: 28px;
        }

        .lri-kicker {
            color: var(--lri-red);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .lri-title {
            font-size: clamp(42px, 6vw, 72px);
            line-height: 0.94;
            font-weight: 850;
            color: var(--lri-ink);
            margin: 0 0 16px;
        }

        .lri-subtitle {
            max-width: 650px;
            font-size: 17px;
            line-height: 1.55;
            color: var(--lri-muted);
            margin: 0;
        }

        .lri-hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 24px;
        }

        .lri-cta,
        .lri-ghost-cta {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 42px;
            padding: 0 15px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .lri-cta {
            background: #111111;
            color: #fffdf8;
            box-shadow: 0 14px 26px rgba(17,17,17,0.16);
        }

        .lri-ghost-cta {
            border: 1px solid var(--lri-line);
            color: var(--lri-ink);
            background: rgba(255,253,248,0.72);
        }

        .lri-object-stage {
            min-height: 250px;
            border: 1px solid var(--lri-line);
            background:
                linear-gradient(145deg, rgba(255,255,255,0.88), rgba(243,238,226,0.92));
            box-shadow: var(--lri-shadow);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px;
        }

        .lri-object-stage:before {
            content: "";
            position: absolute;
            inset: 18px;
            border: 1px solid rgba(23,23,23,0.08);
            border-radius: 8px;
        }

        .lri-object-stage:after {
            content: "RESALE INTELLIGENCE";
            position: absolute;
            left: 22px;
            bottom: 18px;
            font-size: 10px;
            letter-spacing: 0.18em;
            color: rgba(23,23,23,0.42);
            font-weight: 700;
        }

        .lri-logo-plinth {
            position: relative;
            z-index: 1;
            width: min(72%, 250px);
            aspect-ratio: 1 / 1;
            border-radius: 10px;
            background:
                linear-gradient(145deg, rgba(255,255,255,0.76), rgba(249,246,238,0.84));
            border: 1px solid rgba(23,23,23,0.10);
            box-shadow:
                0 24px 52px rgba(23,23,23,0.12),
                inset 0 1px 0 rgba(255,255,255,0.70);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .lri-logo-plinth:before {
            content: "";
            position: absolute;
            inset: 12px;
            border-radius: 8px;
            border: 1px solid rgba(23,23,23,0.08);
        }

        .lri-lego-logo {
            position: relative;
            z-index: 1;
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 7px;
            box-shadow: 0 18px 34px rgba(185,28,28,0.24);
        }

        .lri-stat-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin: 24px 0;
        }

        .lri-stat {
            border: 1px solid var(--lri-line);
            background: rgba(255,253,248,0.78);
            border-radius: 8px;
            padding: 17px;
            min-height: 112px;
            box-shadow: var(--lri-shadow);
        }

        .lri-stat-value {
            font-size: 32px;
            line-height: 1;
            font-weight: 850;
            color: var(--lri-ink);
            margin-bottom: 9px;
        }

        .lri-stat-label {
            color: var(--lri-muted);
            font-size: 12px;
            line-height: 1.4;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            font-weight: 750;
        }

        .lri-editorial-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin: 18px 0;
        }

        .lri-editorial-card {
            border: 1px solid var(--lri-line);
            background: var(--lri-surface);
            border-radius: 8px;
            padding: 20px;
            min-height: 190px;
            box-shadow: var(--lri-shadow);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        .lri-editorial-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 24px 50px rgba(23,23,23,0.10);
        }

        .lri-card-index {
            color: var(--lri-red);
            font-size: 11px;
            font-weight: 850;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 18px;
        }

        .lri-card-title {
            font-size: 21px;
            line-height: 1.08;
            color: var(--lri-ink);
            font-weight: 850;
            margin-bottom: 10px;
        }

        .lri-card-copy {
            font-size: 14px;
            line-height: 1.55;
            color: var(--lri-muted);
        }

        .lri-panel {
            border: 1px solid var(--lri-line);
            background: rgba(255,253,248,0.92);
            border-radius: 8px;
            box-shadow: var(--lri-shadow);
            padding: 22px;
            margin: 18px 0;
        }

        .lri-input-intro {
            border: 1px solid var(--lri-line);
            background: rgba(255,253,248,0.92);
            border-radius: 8px 8px 0 0;
            box-shadow: 0 14px 34px rgba(23,23,23,0.06);
            padding: 20px 22px;
            margin: 18px 0 0;
        }

        .lri-input-copy {
            color: var(--lri-muted);
            font-size: 14px;
            line-height: 1.45;
            max-width: 620px;
        }

        .lri-section-label {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--lri-line);
            color: var(--lri-muted);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }

        .lri-result-grid {
            display: grid;
            grid-template-columns: minmax(210px, 0.8fr) minmax(0, 1.2fr);
            gap: 18px;
            margin-top: 18px;
            min-width: 0;
        }

        .lri-score-card {
            border: 1px solid var(--lri-line);
            background: linear-gradient(180deg, #171717, #24211d);
            color: #fffdf8;
            border-radius: 8px;
            padding: 22px;
            min-height: 215px;
            box-shadow: 0 20px 50px rgba(23,23,23,0.18);
            width: 100%;
            min-width: 0;
        }

        .lri-score-number {
            font-size: 72px;
            line-height: 0.9;
            font-weight: 850;
            margin-top: 16px;
        }

        .lri-score-label {
            color: rgba(255,253,248,0.66);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-weight: 800;
        }

        .lri-category {
            display: inline-flex;
            align-items: center;
            margin-top: 16px;
            padding: 7px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
        }

        .lri-category.GREEN { color: #e9fff6; background: rgba(17,107,79,0.92); }
        .lri-category.YELLOW { color: #1d1600; background: rgba(214,169,0,0.92); }
        .lri-category.RED { color: #fff1f1; background: rgba(185,28,28,0.92); }

        .lri-metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
        }

        .lri-metric {
            border: 1px solid var(--lri-line);
            border-radius: 8px;
            padding: 15px;
            background: var(--lri-surface);
            transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
            min-width: 0;
        }

        .lri-metric:hover {
            transform: translateY(-2px);
            border-color: rgba(23,23,23,0.22);
            box-shadow: 0 12px 28px rgba(23,23,23,0.08);
        }

        .lri-metric-label {
            color: var(--lri-muted);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 800;
            margin-bottom: 7px;
        }

        .lri-metric-value {
            font-size: 20px;
            line-height: 1.2;
            font-weight: 800;
            color: var(--lri-ink);
            overflow-wrap: anywhere;
        }

        .lri-detail-list {
            display: grid;
            gap: 8px;
            margin-top: 14px;
        }

        .lri-detail-row {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            padding: 10px 0;
            border-bottom: 1px solid rgba(23,23,23,0.08);
            color: var(--lri-muted);
            font-size: 14px;
        }

        .lri-detail-row strong {
            color: var(--lri-ink);
            font-weight: 750;
            text-align: right;
            overflow-wrap: anywhere;
            min-width: 0;
        }

        .lri-risk-list {
            margin-top: 12px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .lri-risk-pill {
            border: 1px solid rgba(185,28,28,0.22);
            background: rgba(185,28,28,0.08);
            color: var(--lri-red);
            border-radius: 999px;
            padding: 7px 10px;
            font-size: 12px;
            font-weight: 700;
        }

        .lri-neutral-pill {
            border: 1px solid rgba(17,107,79,0.22);
            background: rgba(17,107,79,0.08);
            color: var(--lri-green);
            border-radius: 999px;
            padding: 7px 10px;
            font-size: 12px;
            font-weight: 700;
        }

        .lri-breakdown {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 10px;
            margin-top: 14px;
        }

        .lri-breakdown-step {
            border-top: 3px solid var(--lri-black);
            background: var(--lri-surface-2);
            border-radius: 0 0 8px 8px;
            padding: 12px;
            min-height: 86px;
        }

        .lri-breakdown-step .label {
            color: var(--lri-muted);
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .lri-breakdown-step .value {
            font-size: 15px;
            font-weight: 850;
            color: var(--lri-ink);
        }

        .lri-pipeline {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 8px;
            margin-top: 14px;
        }

        .lri-pipeline-step {
            position: relative;
            border: 1px solid var(--lri-line);
            border-radius: 8px;
            background: var(--lri-surface-2);
            padding: 14px;
            min-height: 122px;
        }

        .lri-pipeline-step:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--lri-red);
            border-radius: 8px 8px 0 0;
        }

        .lri-step-number {
            color: var(--lri-muted);
            font-size: 10px;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            font-weight: 850;
            margin-bottom: 12px;
        }

        .lri-step-title {
            color: var(--lri-ink);
            font-size: 15px;
            line-height: 1.15;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .lri-step-copy {
            color: var(--lri-muted);
            font-size: 12px;
            line-height: 1.45;
        }

        .lri-manifesto {
            border-left: 4px solid var(--lri-red);
            background: rgba(255,253,248,0.72);
            padding: 18px 20px;
            margin-top: 14px;
            color: var(--lri-ink);
            font-size: 18px;
            line-height: 1.45;
            font-weight: 750;
        }

        .lri-status-panel {
            display: grid;
            grid-template-columns: 14px minmax(0, 1fr);
            gap: 14px;
            align-items: start;
            border: 1px solid var(--lri-line);
            background: rgba(255,253,248,0.94);
            border-radius: 8px;
            padding: 16px 18px;
            margin: 16px 0;
            box-shadow: 0 14px 34px rgba(23,23,23,0.06);
        }

        .lri-status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--lri-muted);
            margin-top: 5px;
            box-shadow: 0 0 0 5px rgba(111,106,97,0.10);
        }

        .lri-status-panel.success .lri-status-dot,
        .lri-status-panel.empty .lri-status-dot {
            background: var(--lri-green);
            box-shadow: 0 0 0 5px rgba(17,107,79,0.10);
        }

        .lri-status-panel.warning .lri-status-dot {
            background: var(--lri-yellow);
            box-shadow: 0 0 0 5px rgba(214,169,0,0.14);
        }

        .lri-status-panel.error .lri-status-dot {
            background: var(--lri-red);
            box-shadow: 0 0 0 5px rgba(185,28,28,0.12);
        }

        .lri-status-panel.loading .lri-status-dot {
            background: var(--lri-red);
            animation: lri-pulse 1.1s ease-in-out infinite;
        }

        .lri-status-title {
            color: var(--lri-ink);
            font-size: 15px;
            font-weight: 850;
            line-height: 1.25;
            margin-bottom: 4px;
        }

        .lri-status-message {
            color: var(--lri-muted);
            font-size: 13px;
            line-height: 1.45;
        }

        .lri-inspector-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin: 22px 0 10px;
            border: 1px solid var(--lri-line);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(255,253,248,0.96), rgba(249,246,238,0.86));
            box-shadow: 0 12px 28px rgba(23,23,23,0.05);
            padding: 14px 16px;
        }

        .lri-inspector-eyebrow,
        .lri-inspector-note {
            color: var(--lri-muted);
            font-size: 11px;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }

        .lri-inspector-title {
            color: var(--lri-ink);
            font-size: 17px;
            font-weight: 850;
            line-height: 1.2;
            margin-top: 3px;
        }

        .lri-status-control-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin: -2px 0 12px;
            border: 1px solid var(--lri-line);
            border-radius: 8px;
            background: rgba(255,253,248,0.74);
            padding: 14px 16px;
        }

        .lri-status-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 34px;
            padding: 0 12px;
            border-radius: 999px;
            border: 1px solid var(--lri-line);
            color: var(--lri-ink);
            background: var(--lri-surface);
            font-size: 11px;
            font-weight: 850;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .lri-status-badge.watching {
            border-color: rgba(214,169,0,0.42);
            background: rgba(214,169,0,0.12);
            color: #7a5a00;
        }

        .lri-status-badge.bought {
            border-color: rgba(17,107,79,0.42);
            background: rgba(17,107,79,0.12);
            color: var(--lri-green);
        }

        .lri-status-badge.discarded {
            border-color: rgba(185,28,28,0.30);
            background: rgba(185,28,28,0.09);
            color: var(--lri-red);
        }

        .lri-table-note {
            color: var(--lri-muted);
            font-size: 13px;
            line-height: 1.45;
            margin: 2px 0 10px;
            max-width: 760px;
        }

        [data-baseweb="select"] > div {
            border-color: var(--lri-line);
            background: rgba(255,253,248,0.96);
            border-radius: 6px;
            min-height: 46px;
        }

        @keyframes lri-pulse {
            0% { transform: scale(0.86); opacity: 0.68; }
            50% { transform: scale(1.12); opacity: 1; }
            100% { transform: scale(0.86); opacity: 0.68; }
        }

        .stButton > button {
            width: 100%;
            border-radius: 6px;
            border: 1px solid #111111;
            background: #111111;
            color: #fffdf8;
            min-height: 48px;
            font-weight: 800;
            letter-spacing: 0.02em;
            transition: transform 150ms ease, box-shadow 150ms ease, background 150ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: #111111;
            background: #b91c1c;
            color: #fffdf8;
            box-shadow: 0 12px 26px rgba(185,28,28,0.2);
        }

        [data-testid="stTextInput"] input {
            border-radius: 6px;
            border: 1px solid var(--lri-line);
            min-height: 48px;
            background: rgba(255,253,248,0.96);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--lri-line);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: var(--lri-shadow);
            margin-bottom: 16px;
        }

        @media (max-width: 980px) {
            .lri-topline {
                justify-content: flex-start;
            }

            .lri-topline > div:last-child {
                display: none;
            }
        }

        @media (max-width: 860px) {
            .block-container {
                padding-left: 1.1rem;
                padding-right: 1.1rem;
                padding-top: 1.2rem;
            }

            .lri-hero,
            .lri-result-grid {
                grid-template-columns: 1fr;
            }

            .lri-metric-grid,
            .lri-breakdown,
            .lri-stat-grid,
            .lri-editorial-grid,
            .lri-pipeline {
                grid-template-columns: 1fr;
            }

            .lri-title {
                font-size: 42px;
            }

            .lri-object-stage {
                min-height: 220px;
                padding: 22px;
            }

            .lri-logo-plinth {
                width: min(58%, 210px);
            }

            .lri-section-label,
            .lri-inspector-panel,
            .lri-status-control-panel {
                align-items: flex-start;
                flex-direction: column;
            }

            .lri-score-number {
                font-size: 58px;
            }

            .lri-score-card {
                min-height: 185px;
            }

            .lri-detail-row {
                display: grid;
                gap: 4px;
            }

            .lri-detail-row strong {
                text-align: left;
            }

            .lri-manifesto {
                font-size: 16px;
            }
        }

        @media (max-width: 560px) {
            .lri-title {
                font-size: 36px;
                line-height: 1;
            }

            .lri-subtitle {
                font-size: 15px;
            }

            .lri-hero-actions {
                display: grid;
                grid-template-columns: 1fr;
            }

            .lri-cta,
            .lri-ghost-cta {
                width: 100%;
            }

            .lri-panel,
            .lri-input-intro,
            .lri-editorial-card,
            .lri-stat {
                padding: 16px;
            }

            .lri-object-stage {
                min-height: 190px;
            }

            .lri-logo-plinth {
                width: min(70%, 190px);
                padding: 18px;
            }

            .lri-pipeline-step {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
