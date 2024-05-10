from django.test import SimpleTestCase
from django.template import Context, Template
from unittest.mock import MagicMock

from django_webfacile.checksums import (
    INTEGRITY_CSS,
    INTEGRITY_FAVICON_APPLE,
    INTEGRITY_FAVICON_ICO,
    INTEGRITY_FAVICON_MANIFEST,
    INTEGRITY_FAVICON_SVG,
    INTEGRITY_JS_MODULE,
    INTEGRITY_JS_NOMODULE,
)
from django_webfacile.templatetags.webfacile_tags import concatenate, hyphenate


class WebfacileCssTagTest(SimpleTestCase):
    def test_css_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load webfacile_tags %} {% webfacile_css %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            f'<link rel="stylesheet" href="/static/webfacile/dist/webfacile/webfacile.min.css"  integrity="{ INTEGRITY_CSS }">',  # noqa
            rendered_template,
        )


class WebfacileJsTagTest(SimpleTestCase):
    def test_js_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load webfacile_tags %} {% webfacile_js %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            f"""
            <script type="module" src="/static/webfacile/dist/webfacile/webfacile.module.min.js" integrity="{ INTEGRITY_JS_MODULE }"></script>
            <script nomodule src="/static/webfacile/dist/webfacile/webfacile.nomodule.min.js" integrity="{ INTEGRITY_JS_NOMODULE }"></script>
            """,  # noqa
            rendered_template,
        )


class WebfacileJsTagWithNonceTest(SimpleTestCase):
    def test_js_tag_rendered(self):
        context = Context()
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_js nonce='random-nonce' %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            f"""
            <script type="module" src="/static/webfacile/dist/webfacile/webfacile.module.min.js" integrity="{ INTEGRITY_JS_MODULE }" nonce="random-nonce"></script>
            <script nomodule src="/static/webfacile/dist/webfacile/webfacile.nomodule.min.js" integrity="{ INTEGRITY_JS_NOMODULE }" nonce="random-nonce"></script>
            """,  # noqa
            rendered_template,
        )


class WebfacileFaviconTagTest(SimpleTestCase):
    def test_favicon_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load webfacile_tags %} {% webfacile_favicon %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            f"""
            <link rel="apple-touch-icon" href="/static/webfacile/dist/favicon/apple-touch-icon.png" integrity="{ INTEGRITY_FAVICON_APPLE }" /><!-- 180×180 -->
            <link rel="icon" href="/static/webfacile/dist/favicon/favicon.svg" type="image/svg+xml" integrity="{ INTEGRITY_FAVICON_SVG }" />
            <link rel="shortcut icon" href="/static/webfacile/dist/favicon/favicon.ico" type="image/x-icon" integrity="{ INTEGRITY_FAVICON_ICO }" />
            <!-- 32×32 -->
            <link rel="manifest" href="/static/webfacile/dist/favicon/manifest.webmanifest"
            crossorigin="use-credentials" integrity="{ INTEGRITY_FAVICON_MANIFEST }" />
            """,  # noqa
            rendered_template,
        )


class WebfacileThemeModaleTagTest(SimpleTestCase):
    def test_theme_modale_tag_rendered(self):
        context = Context()
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_theme_modale %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
            <h1 id="webfacile-theme-modal-title" class="webfacile-modal__title">
                Paramètres d’affichage
            </h1>
            """,
            rendered_template,
        )


class WebfacileAccordionTagTest(SimpleTestCase):
    test_data = {
        "id": "sample-accordion",
        "title": "Title of the accordion item",
        "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_accordion test_data %}"
    )

    def test_accordion_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <section class="webfacile-accordion">
                <h3 class="webfacile-accordion__title">
                    <button type="button" class="webfacile-accordion__btn" aria-expanded="false" aria-controls="sample-accordion">Title of the accordion item</button>
                </h3>
                <div class="webfacile-collapse" id="sample-accordion">
                    <p><b>Bold</b> and <em>emphatic</em> Example content</p>
                </div>
            </section>
            """,  # noqa
            rendered_template,
        )


class WebfacileAccordionGroupTagTest(SimpleTestCase):
    test_data = [
        {
            "id": "sample-accordion",
            "title": "Title of the accordion item",
            "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
        },
        {
            "id": "sample-accordion-2",
            "title": "Title of the second accordion item",
            "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
        },
        {
            "id": "sample-accordion-3",
            "title": "Title of the third accordion item",
            "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
        },
    ]

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_accordion_group test_data %}"
    )

    def test_accordion_group_count(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<p><b>Bold</b> and <em>emphatic</em> Example content</p>""",
            rendered_template,
            count=3,
        )


class WebfacileAlertTagTest(SimpleTestCase):
    test_data = {
        "title": "Sample title",
        "type": "info",
        "content": "Sample content",
        "heading_tag": "h3",
        "is_collapsible": True,
        "id": "test-alert-message",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_alert test_data %}"
    )

    def test_alert_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML("""<p>Sample content</p>""", rendered_template)

    def test_alert_tag_heading_can_be_set(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<h3 class="webfacile-alert__title">Sample title</h3>""", rendered_template
        )

    def test_alert_tag_has_collapse_button(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <button class="webfacile-btn--close webfacile-btn" title="Masquer le message" onclick="const alert = this.parentNode; alert.parentNode.removeChild(alert)">
              Masquer le message
            </button>
            """,  # noqa
            rendered_template,
        )


class WebfacileBadgeTagTest(SimpleTestCase):
    test_data = {
        "label": "badge label",
        "extra_classes": "webfacile-badge--success",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_badge test_data %}"
    )

    def test_badge_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <p class="webfacile-badge webfacile-badge--success">badge label</p>
            """,
            rendered_template,
        )


class WebfacileBreadcrumbTagTest(SimpleTestCase):
    breadcrumb_data = {
        "links": [{"url": "test-url", "title": "Test title"}],
        "current": "Test page",
    }

    context = Context({"breadcrumb_data": breadcrumb_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_breadcrumb breadcrumb_data %}"
    )

    def test_breadcrumb_tag_current_page(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<a class="webfacile-breadcrumb__link" aria-current="page">Test page</a>""",
            rendered_template,
        )

    def test_breadcrumb_tag_middle_link(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<a class="webfacile-breadcrumb__link" href="test-url">Test title</a>""",
            rendered_template,
        )


class WebfacileButtonTagTest(SimpleTestCase):
    test_data = {
        "onclick": "alert('test button action')",
        "label": "button label",
        "type": "button",
        "name": "test-button",
        "extra_classes": "webfacile-btn--secondary",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_button test_data %}"
    )

    def test_button_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <button
            class="webfacile-btn webfacile-btn--secondary"
            onclick="alert(&#x27;test button action&#x27;)"
            type="button"
            name="test-button"
            >
                button label
            </button>
            """,
            rendered_template,
        )


class WebfacileButtonGroupTagTest(SimpleTestCase):
    test_data = {
        "extra_classes": "webfacile-btns-group--equisized",
        "items": [
            {
                "onclick": "alert('test button action')",
                "label": "Button label",
                "type": "button",
                "name": "test-button",
                "extra_classes": "",
            },
            {
                "onclick": "alert('test button action')",
                "label": "Button 2 label",
                "type": "button",
                "name": "test-button-2",
                "extra_classes": "webfacile-btn--secondary",
            },
        ],
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_button_group test_data %}"
    )

    def test_button_group_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <ul class="webfacile-btns-group webfacile-btns-group--equisized">
                <li>
                    <button class="webfacile-btn"
                        onclick="alert(&#x27;test button action&#x27;)"
                        type="button"
                        name="test-button">
                    Button label
                    </button>
                </li>

                <li>
                    <button class="webfacile-btn webfacile-btn--secondary"
                        onclick="alert(&#x27;test button action&#x27;)"
                        type="button"
                        name="test-button-2">
                        Button 2 label
                    </button>
                </li>
            </ul>
            """,
            rendered_template,
        )


class WebfacileCalloutTagTest(SimpleTestCase):
    test_data = {
        "text": "Text of the callout item",
        "title": "Title of the callout item",
        "icon_class": "webfacile-icon-information-line",
        "heading_tag": "h4",
        "button": {"onclick": "close()", "label": "button label", "type": "button"},
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_callout test_data %}"
    )

    def test_callout_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
    <p class="webfacile-callout__text">
        Text of the callout item
    </p>""",
            rendered_template,
        )

    def test_callout_optional_title_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<h4 class="webfacile-callout__title">Title of the callout item</h4>""",
            rendered_template,
        )

    def test_callout_optional_icon_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue("webfacile-icon-information-line" in rendered_template)

    def test_callout_optional_button_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <button
                type="button"
                class="webfacile-btn"
                onclick="close()"
            >
                button label
            </button>
            """,
            rendered_template,
        )


class WebfacileCardTagTest(SimpleTestCase):
    card_data = {
        "top_detail": {"detail": {"text": "Appears before the title of the card item"}},
        "title": "Title of the card item",
        "description": "Text of the card item",
        "image_url": "https://test.gouv.fr/test.png",
        "link": "https://test.gouv.fr",
    }

    extra_classes = "test-extraclass"
    new_tab = True

    context = Context(
        {"card_data": card_data, "extra_classes": extra_classes, "new_tab": new_tab}
    )
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_card card_data extra_classes=extra_classes new_tab=newtab %}"  # noqa
    )

    def test_card_is_created(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue("webfacile-card" in rendered_template)

    def test_card_has_detail(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            '<p class="webfacile-card__detail">Appears before the title of the card item</p>',
            rendered_template,
        )

    def test_card_has_title(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
                <p class="webfacile-card__title">
                <a href="https://test.gouv.fr" target="_self">
                    Title of the card item
                </a>
            </p>""",
            rendered_template,
        )

    def test_card_has_description(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            '<p class="webfacile-card__desc">Text of the card item</p>',
            rendered_template,
        )

    def test_card_has_optional_image(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-card__img">
                <img src="https://test.gouv.fr/test.png" class="webfacile-responsive-img" alt="">
            </div>
            """,  # noqa
            rendered_template,
        )


class WebfacileConsentTagTest(SimpleTestCase):
    test_data = {
        "title": "À propos des cookies sur Django-webfacile",
        "content": """
                Bienvenue ! Nous utilisons des cookies pour améliorer votre expérience et les
                services disponibles sur ce site. Pour en savoir plus, visitez la page <a href="#">
                Données personnelles et cookies</a>. Vous pouvez, à tout moment, avoir le contrôle
                sur les cookies que vous souhaitez activer.
                """,
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_consent test_data %}"
    )

    def test_consent_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-consent-banner">
            <h2 class="webfacile-h6">
                À propos des cookies sur Django-webfacile
            </h2>
            <div class="webfacile-consent-banner__content">
                <p class="webfacile-text--sm">
                    Bienvenue ! Nous utilisons des cookies pour améliorer votre expérience et les
                    services disponibles sur ce site. Pour en savoir plus, visitez la page <a href="#">
                    Données personnelles et cookies</a>. Vous pouvez, à tout moment, avoir le contrôle
                    sur les cookies que vous souhaitez activer.
                </p>
            </div>
            <ul class="webfacile-consent-banner__buttons webfacile-btns-group webfacile-btns-group--right webfacile-btns-group--inline-reverse webfacile-btns-group--inline-sm">
                <li>
                <button class="webfacile-btn"
                        id="consent-accept-all"
                        title="Autoriser tous les cookies">
                    Tout accepter
                </button>
                </li>
                <li>
                <button class="webfacile-btn"
                        id="consent-reject-all"
                        title="Refuser tous les cookies">
                    Tout refuser
                </button>
                </li>
                <li>
                <button class="webfacile-btn webfacile-btn--secondary"
                        id="consent-customize"
                        data-webfacile-opened="false"
                        aria-controls="webfacile-consent-modal"
                        title="Personnaliser les cookies">
                    Personnaliser
                </button>
                </li>
            </ul>
            </div>
            """,
            rendered_template,
        )


class WebfacileContentTagTest(SimpleTestCase):
    test_data = {
        "alt_text": "Silhouette stylisée représentant le soleil au-dessus de deux montagnes.",
        "caption": "Image en largeur normale et en 4x3",
        "image_url": "/static/img/placeholder.16x9.svg",
        "ratio_class": "webfacile-ratio-4x3",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_content test_data %}"
    )

    def test_content_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <figure class="webfacile-content-media" role="group" aria-label="Image en largeur normale et en 4x3">
            <div class="webfacile-content-media__img">
                <img class="webfacile-responsive-img webfacile-ratio-4x3"
                    src="/static/img/placeholder.16x9.svg"
                    alt="Silhouette stylisée représentant le soleil au-dessus de deux montagnes." />
            </div>
                <figcaption class="webfacile-content-media__caption">
                Image en largeur normale et en 4x3
                </figcaption>
            </figure>""",
            rendered_template,
        )


class WebfacileFranceConnectTagTest(SimpleTestCase):
    test_data = {"id": "france-connect"}

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_france_connect test_data %}"
    )

    def test_franceconnect_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-connect-group">
                <button class="webfacile-connect"
                        id="france-connect">
                    <span class="webfacile-connect__login">S’identifier avec</span>
                    <span class="webfacile-connect__brand">FranceConnect</span>
                </button>
                <p>
                    <a href="https://franceconnect.gouv.fr/"
                        target="_blank"
                        rel="noopener"
                        title="Qu’est-ce que FranceConnect ? - Ouvre une nouvelle fenêtre">Qu’est-ce que FranceConnect ?</a>
                </p>
            </div>
            """,
            rendered_template,
        )


class WebfacileFranceConnectPlusTagTest(SimpleTestCase):
    test_data = {"id": "france-connect-plus", "plus": True}

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_france_connect test_data %}"
    )

    def test_franceconnectplus_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-connect-group">
                <button class="webfacile-connect webfacile-connect--plus"
                        id="france-connect-plus">
                    <span class="webfacile-connect__login">S’identifier avec</span>
                    <span class="webfacile-connect__brand">FranceConnect</span>
                </button>
                <p>
                    <a href="https://franceconnect.gouv.fr/france-connect-plus"
                        target="_blank"
                        rel="noopener"
                        title="Qu’est-ce que FranceConnect+ ? - Ouvre une nouvelle fenêtre">Qu’est-ce que FranceConnect+ ?</a>
                </p>
            </div>
            """,
            rendered_template,
        )


class WebfacileHighlightTagTest(SimpleTestCase):
    test_data = {
        "content": "Content of the highlight item (can include html)",
        "title": "(Optional) Title of the highlight item",
        "heading_tag": "h4",
        "size_class": "webfacile-text--sm",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_highlight test_data %}"
    )

    def test_highlight_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-highlight">
                <p class="webfacile-text--sm">
                    Content of the highlight item (can include html)
                </p>
            </div>
            """,
            rendered_template,
        )


class WebfacileInputTagTest(SimpleTestCase):
    test_data_text = {
        "id": "sample-id",
        "label": "Label of the input item",
        "type": "text",
        "onchange": "doStuff()",
        "value": "Sample value",
    }

    test_data_date = {
        "id": "sample-id",
        "label": "Label of the input item",
        "type": "date",
        "onchange": "doStuff()",
        "value": "2021-09-15",
        "min": "2021-09-03",
        "max": "2021-04-21",
    }

    def test_text_input_tag_rendered(self):
        context = Context({"test_data": self.test_data_text})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_input test_data %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
            <div class="webfacile-input-group ">
                <label class="webfacile-label" for="sample-id">
                Label of the input item
                </label>
                <input
                    class="webfacile-input"
                    type="text"
                    id="sample-id"
                    name="sample-id"
                    onchange="doStuff()"
                    value="Sample value"
                />
            </div>
            """,
            rendered_template,
        )

    def test_date_input_tag_rendered(self):
        context = Context({"test_data": self.test_data_date})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_input test_data %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
            <div class="webfacile-input-group ">
                <label class="webfacile-label" for="sample-id">
                Label of the input item
                </label>
                <input
                    class="webfacile-input"
                    type="date"
                    id="sample-id"
                    name="sample-id"
                    onchange="doStuff()"
                    value="2021-09-15"
                    min="2021-09-03"
                    max="2021-04-21"
                />
            </div>
            """,
            rendered_template,
        )


class WebfacileLinkTagTest(SimpleTestCase):
    test_data = {
        "url": "http://example.com",
        "label": "Label of the link item",
        "is_external": True,
        "extra_classes": "webfacile-link--lg",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_link test_data %}"
    )

    def test_link_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <a
            class="webfacile-link webfacile-icon-external-link-line webfacile-link--icon-right webfacile-link--lg"
            href="http://example.com"
            target="_blank" rel="noopener noreferrer"
            >
              Label of the link item <span class="webfacile-sr-only">Ouvre une nouvelle fenêtre</span>
            </a>
            """,  # noqa
            rendered_template,
        )


class WebfacileNoticeTagTest(SimpleTestCase):
    test_data = {
        "title": """Bandeau d’information importante avec <a href='#'
                            rel='noopener external'
                            title="intitulé - Ouvre une nouvelle fenêtre" target='_blank'>
                            lien</a>.""",
        "is_collapsible": True,
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_notice test_data %}"
    )

    def test_notice_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-notice__body">
                <p class="webfacile-notice__title">
                    Bandeau d’information importante avec <a href='#'
                        rel='noopener external'
                        title="intitulé - Ouvre une nouvelle fenêtre" target='_blank'>
                        lien</a>.
                </p>
                    <button class="webfacile-btn--close webfacile-btn"
                        title="Masquer le message"
                        onclick="const notice = this.parentNode.parentNode.parentNode; notice.parentNode.removeChild(notice)">
                    Masquer le message
                    </button>
                </div>
            """,  # noqa
            rendered_template,
        )


class WebfacileQuoteTagTest(SimpleTestCase):
    test_data = {
        "text": "Développer vos sites et applications en utilisant des composants prêts à l'emploi, accessibles et ergonomiques",  # noqa
        "source_url": "https://www.systeme-de-design.gouv.fr/",
        "author": "Auteur",
        "source": "Système de Design de l'État",
        "details": [
            {"text": "Détail sans lien"},
            {
                "text": "Détail avec lien",
                "link": "https://template.incubateur.net/",
            },
        ],
        "image_url": "https://via.placeholder.com/150x150",
    }
    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_quote test_data %}"
    )

    def test_quote_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <figure class="webfacile-quote webfacile-quote--column">
                <blockquote cite="https://www.systeme-de-design.gouv.fr/">
                    <p>Développer vos sites et applications en utilisant des composants prêts à l&#x27;emploi, accessibles et ergonomiques</p>
                </blockquote>
                <figcaption>
                    <p class="webfacile-quote__author">Auteur</p>
                    <ul class="webfacile-quote__source">
                    <li>
                        <cite>Système de Design de l&#x27;État</cite>
                    </li>
                    <li>Détail sans lien</li>
                    <li><a target="_blank" rel="noopener noreferrer" href="https://template.incubateur.net/">Détail avec lien <span class="webfacile-sr-only">Ouvre une nouvelle fenêtre</span></a></li>
                    </ul>
                    <div class="webfacile-quote__image">
                    <img src="https://via.placeholder.com/150x150" class="webfacile-responsive-img" alt="" />
                    </div>
                </figcaption>
            </figure>
            """,  # noqa
            rendered_template,
        )


class WebfacileSidemenuTagTest(SimpleTestCase):
    test_data = {
        "title": "Menu",
        "heading_tag": "h2",
        "items": [
            {
                "label": "Menu replié",
                "items": [
                    {
                        "label": "Une page",
                        "link": "#",
                    },
                    {
                        "label": "Une autre page",
                        "link": "/sidemenu",
                    },
                ],
            },
            {
                "label": "Menu ouvert",
                "items": [
                    {
                        "label": "Sous-menu replié",
                        "items": [
                            {"label": "Encore une page", "link": "#"},
                        ],
                    },
                    {
                        "label": "Sous-menu ouvert",
                        "items": [
                            {"label": "Page non active", "link": "#"},
                            {
                                "label": "Page active",
                                "link": "/django-webfacile/components/sidemenu/",
                            },
                        ],
                    },
                ],
            },
        ],
    }

    request_mock = MagicMock()
    request_mock.path = "/django-webfacile/components/sidemenu/"
    context = Context({"request": request_mock, "test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_sidemenu test_data %}"
    )
    rendered_template = template_to_render.render(context)

    def test_sidemenu_tag_rendered(self):
        self.assertInHTML(
            """
            <li class="webfacile-sidemenu__item">
                <a class="webfacile-sidemenu__link" href="#" target="_self" >Une page</a>
            </li>

            """,
            self.rendered_template,
        )

    def test_sidemenu_heading_can_be_set(self):
        self.assertInHTML(
            """
            <h2 class="webfacile-sidemenu__title">Menu</h2>
            """,
            self.rendered_template,
        )

    def test_sidemenu_tag_current_page_and_parents_are_active(self):
        self.assertInHTML(
            """
            <li class="webfacile-sidemenu__item webfacile-sidemenu__item--active">
                <button
                    type="button"
                    class="webfacile-sidemenu__btn"
                    aria-expanded="true"
                    aria-controls="webfacile-sidemenu-item-2-2"
                >
                    Sous-menu ouvert
                </button>
                <div class="webfacile-collapse" id="webfacile-sidemenu-item-2-2">
                    <ul class="webfacile-sidemenu__list">
                        <li class="webfacile-sidemenu__item">
                        <a class="webfacile-sidemenu__link" href="#" target="_self" >
                            Page non active
                        </a>
                        </li>

                        <li class="webfacile-sidemenu__item webfacile-sidemenu__item--active">
                        <a class="webfacile-sidemenu__link" href="/django-webfacile/components/sidemenu/" target="_self"  aria-current="page">
                            Page active
                        </a>
                        </li>
                    </ul>
                </div>
            </li>
            """,  # noqa
            self.rendered_template,
        )


class WebfacileSummaryTagTest(SimpleTestCase):
    test_data = [
        {"link": "link 1", "label": "First item title"},
        {"link": "link 2", "label": "Second item title"},
    ]

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_summary test_data %}"
    )

    def test_summary_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <nav role="navigation" class="webfacile-summary" aria-labelledby="webfacile-summary-title">
                <p class="webfacile-summary__title" id="webfacile-summary-title">Sommaire</p>
                <ol class="webfacile-summary__list">

                    <li>
                        <a class="webfacile-summary__link" href="link 1">First item title</a>
                    </li>

                    <li>
                        <a class="webfacile-summary__link" href="link 2">Second item title</a>
                    </li>
                </ol>
            </nav>
            """,  # noqa
            rendered_template,
        )


class WebfacileSkiplinksTagTest(SimpleTestCase):
    test_data = [
        {"link": "#contenu", "label": "Contenu"},
        {"link": "#header-navigation", "label": "Menu"},
    ]

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_skiplinks test_data %}"
    )

    def test_summary_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-skiplinks">
                <nav role="navigation" class="webfacile-container" aria-label="Accès rapide">
                    <ul class="webfacile-skiplinks__list">
                    <li>
                        <a class="webfacile-link" href="#contenu">Contenu</a>
                    </li>
                    <li>
                        <a class="webfacile-link" href="#header-navigation">Menu</a>
                    </li>
                    </ul>
                </nav>
            </div>
            """,
            rendered_template,
        )


class WebfacileTagTagTest(SimpleTestCase):
    def test_basic_tag_rendered(self):
        test_data = {
            "label": "Label of the tag item",
        }

        context = Context({"test_data": test_data})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_tag test_data %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """<p class="webfacile-tag">Label of the tag item</p>""", rendered_template
        )

    def test_tag_with_link_rendered(self):
        test_data = {"label": "Label of the tag item", "link": "/components"}

        context = Context({"test_data": test_data})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_tag test_data %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """<a href="/components" class="webfacile-tag">Label of the tag item</a>""",
            rendered_template,
        )

    def test_tag_with_icon_rendered(self):
        test_data = {"label": "Label of the tag item"}

        context = Context({"test_data": test_data})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_tag test_data extra_classes='webfacile-icon-arrow-right-line webfacile-tag--icon-left' %}"  # noqa
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """<p class="webfacile-tag webfacile-icon-arrow-right-line webfacile-tag--icon-left">Label of the tag item</p>""",  # noqa
            rendered_template,
        )

    def test_tag_with_action_rendered(self):
        test_data = {
            "label": "Label of the tag item",
            "link": "#",
            "onclick": "console.log('clicked');",
        }

        context = Context({"test_data": test_data})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_tag test_data %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """<a href="#" class="webfacile-tag" onclick="console.log(&#x27;clicked&#x27;);">Label of the tag item</a>""",  # noqa
            rendered_template,
        )


class WebfacileToggleTagTest(SimpleTestCase):
    def test_toggle_rendered(self):
        test_data = {
            "label": "Interrupteur complet aligné à gauche",
            "help_text": "Cet interrupteur présente toutes les options disponibles",
            "is_disabled": False,
            "extra_classes": "webfacile-toggle--label-left webfacile-toggle--border-bottom",
            "id": "toggle-full",
        }

        context = Context({"test_data": test_data})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_toggle test_data %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
            <div class="webfacile-toggle webfacile-toggle--label-left webfacile-toggle--border-bottom">
                <input type="checkbox"
                        class="webfacile-toggle__input"
                        aria-describedby="toggle-full-hint-text"
                        id="toggle-full">
                <label class="webfacile-toggle__label"
                        for="toggle-full"
                        data-webfacile-checked-label="Activé"
                        data-webfacile-unchecked-label="Désactivé">
                    Interrupteur complet aligné à gauche
                </label>
                    <p class="webfacile-hint-text" id="toggle-full-hint-text">
                    Cet interrupteur présente toutes les options disponibles
                    </p>
                </div>
            """,
            rendered_template,
        )


class WebfacileTooltipTagTest(SimpleTestCase):
    def test_tooltip_rendered(self):
        test_data = {
            "content": "Contenu d’une infobule activée au survol",
            "label": "Libellé du lien",
            "id": "tooltip-test",
        }

        context = Context({"test_data": test_data})
        template_to_render = Template(
            "{% load webfacile_tags %} {% webfacile_tooltip test_data %}"
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
            <a class="webfacile-link"
                aria-describedby="tooltip-test"
                id="link-tooltip-test"
                href="#">
                Libellé du lien
            </a>

            <span class="webfacile-tooltip webfacile-placement"
                id="tooltip-test"
                role="tooltip"
                aria-hidden="true">Contenu d’une infobule activée au survol</span>
            """,
            rendered_template,
        )


class WebfacileTranscriptionTagTest(SimpleTestCase):
    test_data = {
        "content": "<div><p>Courte transcription basique</p></div>",
        "id": "transcription-test",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load webfacile_tags %} {% webfacile_transcription test_data %}"
    )

    def test_summary_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
            <div class="webfacile-transcription">
                <button class="webfacile-transcription__btn"
                        aria-expanded="false"
                        aria-controls="webfacile-transcription__collapse-transcription-test">
                    Transcription
                </button>
                <div class="webfacile-collapse" id="webfacile-transcription__collapse-transcription-test">
                    <div class="webfacile-transcription__footer">
                        <div class="webfacile-transcription__actions-group">

                            <button class="webfacile-btn webfacile-btn--fullscreen"
                                    aria-controls="webfacile-transcription-modal-transcription-test"
                                    data-webfacile-opened="false"
                                    title="Agrandir">
                                Agrandir
                            </button>
                        </div>
                    </div>
                    <dialog id="webfacile-transcription-modal-transcription-test"
                            class="webfacile-modal"
                            role="dialog"
                            aria-labelledby="webfacile-transcription-modal-transcription-test-title">
                        <div class="webfacile-container webfacile-container--fluid facile-container-md">
                            <div class="webfacile-grid-row webfacile-grid-row--center">
                                <div class="webfacile-col-12 webfacile-col-md-10 webfacile-col-lg-8">
                                    <div class="webfacile-modal__body">
                                        <div class="webfacile-modal__header">

                                            <button class="webfacile-btn--close webfacile-btn"
                                                    aria-controls="webfacile-transcription-modal-transcription-test"
                                                    title="Fermer">
                                                Fermer
                                            </button>
                                        </div>
                                        <div class="webfacile-modal__content">
                                            <h1 id="webfacile-transcription-modal-transcription-test-title"
                                                class="webfacile-modal__title">
                                                Transcription
                                            </h1>
                                            <div><p>Courte transcription basique</p></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </dialog>
                </div>
            </div>
            """,  # noqa
            rendered_template,
        )


class ConcatenateTestCase(SimpleTestCase):
    def test_normal_concatenation(self):
        result = concatenate("test ", "value")
        self.assertEqual(result, "test value")

    def test_concatenation_with_empty_string(self):
        result = concatenate("test ", "")
        self.assertEqual(result, "test ")

    def test_concatenation_with_a_number(self):
        result = concatenate("test ", 3)
        self.assertEqual(result, "test 3")


class HyphenateTestCase(SimpleTestCase):
    def test_normal_hyphenation(self):
        result = hyphenate("test", "value")
        self.assertEqual(result, "test-value")

    def test_empty_value_is_not_hyphenated(self):
        result = hyphenate("test", "")
        self.assertEqual(result, "test")

    def test_numbers_can_be_hyphenated(self):
        result = hyphenate(4, 3)
        self.assertEqual(result, "4-3")

    def test_numbers_and_string_can_be_hyphenated(self):
        result = hyphenate("test", 3)
        self.assertEqual(result, "test-3")