import logging
from typing import Final, Optional

import cssutils
from bs4 import BeautifulSoup
from cssutils.css import CSSStyleSheet, CSSMediaRule, CSSRule, CSSStyleRule

cssutils.log.setLevel(logging.FATAL)
MEDIA_TEXT: Final[str] = "(prefers-color-scheme: dark)"
SVG_SELECTOR: Final[str] = "svg"
INVERT_RULE: Final[str] = "filter: invert(100%)"
FILTER_PROPERTY: Final[str] = "invert(100%);"


def add_style(file: str) -> None:
    with open(file, "r") as handle:
        contents = handle.read()
    xml = BeautifulSoup(contents, "xml")
    # check if we have a svg tag
    if not xml.svg:
        raise ValueError(f"Missing svg tag in '{file}'")
    # See if there is already a style
    style_tag = xml.svg.find('style')
    if not style_tag:
        style_tag = xml.new_tag('style')
        xml.svg.append(style_tag)
    # Parse the style tag
    style = style_tag.string if style_tag.string is not None else ""
    stylesheet: CSSStyleSheet = cssutils.parseString(style)
    darkmode_style: Optional[CSSMediaRule] = None
    svg_style: Optional[CSSStyleRule] = None
    for rule in stylesheet.cssRules:
        # Check if it contains a media query
        if rule.type == CSSRule.MEDIA_RULE:
            # Check if the media query is for dark mode
            if rule.media.mediaText == MEDIA_TEXT:
                darkmode_style = rule
                # Check if there is a rule for 'svg *'
                for css_rule in rule.cssRules:
                    if css_rule.selectorText == SVG_SELECTOR:
                        svg_style = css_rule
                        if INVERT_RULE not in css_rule.style.cssText:
                            css_rule.style["filter"] = FILTER_PROPERTY
                        break

    if not darkmode_style:
        darkmode_style = CSSMediaRule(MEDIA_TEXT, parentStyleSheet=stylesheet)
        stylesheet.add(darkmode_style)
    if not svg_style:
        svg_style = CSSStyleRule(SVG_SELECTOR, parentRule=darkmode_style, parentStyleSheet=stylesheet)
        svg_style.style["filter"] = FILTER_PROPERTY
        darkmode_style.add(svg_style)
    style_tag.string = stylesheet.cssText.decode("utf-8")
    with open(file, 'w') as handle:
        handle.write(str(xml))
