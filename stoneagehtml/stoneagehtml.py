#!/usr/bin/env python

"""
Stone-Age HTML Filter: prepare documents for e-mail distribution.

    Copyright (C) 2007 Malthe Borch

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

usage:

  stoneagehtml.compactify(text)

  (see function def for details)

"""

from bs4 import BeautifulSoup

import cssutils
import logging
import re
import sys
import warnings


# regex: selectors
regex_selector_id = re.compile(r"((?:\.|#)[\w\-_]+)")
regex_selector = re.compile(r"(\w+)?(#([\w\-_]+))?(\.([\w\-_]+))?(\*)?")

# regex: compound css-tags
regex_tags = {
    "background": re.compile(
        r"^ *((?!url)(?P<color>[#\w]+))? *((?P<image>url *\([^\)]+\)) *"
        + r"(?P<repeat>(no-)?repeat(-(x|xy|y))?)? *"
        + r"(?P<attachment>(scroll|fixed))? *"
        + r"(?P<position>(top|bottom|left|center|right| |[-\w%]+)+)?)?"
    ),
}

# default tag black-list based on Google Mail's style filter
tag_blacklist = [
    "visibility",
    "font-family",
    "height",
    "list-style-image",
    "top",
    "bottom",
    "left",
    "right",
    "z-index",
    "position",
    "background-image",
    "background-repeat",
    "background-position",
]

cssutils.log.setLevel(logging.CRITICAL)

# CSSUTILS PREFERENCES
cssutils.ser.prefs.keepAllProperties = False
cssutils.ser.prefs.keepComments = False
cssutils.ser.prefs.keepEmptyRules = False
cssutils.ser.prefs.keepUnknownAtRules = False
cssutils.ser.prefs.keepUsedNamespaceRulesOnly = True
cssutils.ser.prefs.resolveVariables = True
cssutils.ser.prefs.validOnly = True


IS_PY2 = sys.version_info[0] == 2


def safe_text(value, encoding="utf-8"):
    """Converts a value to text, even if is already a text string.

    Taken from Products.CMFPlone.utils

    >>> test_bytes = u'\u01b5'.encode('utf-8')
    >>> safe_text('spam') == u'spam'
    True
    >>> safe_text(b'spam') == u'spam'
    True
    >>> safe_text(u'spam') == u'spam'
    True
    >>> safe_text(u'spam'.encode('utf-8')) == u'spam'
    True
    >>> safe_text(test_bytes) == u'\u01b5'
    True
    >>> safe_text(u'\xc6\xb5'.encode('iso-8859-1')) == u'\u01b5'
    True
    >>> safe_text(test_bytes, encoding='ascii') == u'\u01b5'
    True
    >>> safe_text(1) == 1
    True
    >>> print(safe_text(None))
    None
    """
    if IS_PY2:
        if isinstance(value, unicode):
            return value
        elif isinstance(value, basestring):
            try:
                value = unicode(value, encoding)
            except (UnicodeDecodeError):
                value = value.decode("utf-8", "replace")
        return value

    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        try:
            value = str(value, encoding)
        except (UnicodeDecodeError):
            value = value.decode("utf-8", "replace")
    return value


def trim_dictionary(d):
    for key, value in d.copy().items():
        if not value:
            del d[key]

    return d


def find_attribute(key, attrs):
    """ In BeautifulSoup 4 attrs are a dictionary
    """
    warnings.warn("deprecated", DeprecationWarning)
    return attrs.get(key)


def tagQuery(tag, tag_name, attrs):
    """Custom tag matcher. Takes into account that tags can
    have several classes."""
    if tag_name and tag_name != tag.name:
        return False

    for key, value in attrs.items():
        tag_attribute_value = tag.attrs.get(key)
        if not tag_attribute_value:
            return False

        if not isinstance(tag_attribute_value, list):
            tag_attribute_value = tag_attribute_value.split()
        if value in tag_attribute_value:
            continue

        return False

    return True


def compactify(text, *args, **kwargs):
    return CompactifyingSoup(text, features="html.parser").compactify(*args, **kwargs)


class CompactifyingSoup(BeautifulSoup):
    class_prefix = "c"
    id_prefix = "i"

    def compactify(
        self,
        abbreviation_enabled=False,
        styles_in_tags=True,
        filter_tags=True,
        expand_css_properties=True,  # experimental
        remove_classnames_and_ids=False,
        media=(u"screen",),
    ):

        """
        This function processes an HTML-soup with two purposes:

        * To reduce the size by abbreviating class names and identifiers and
          removing unused css-declarations

        * Degrades the markup detail to provide compatibility with browsers
          and interface which do not support the full CSS ruleset.

        This is demonstrated below.

        >>> text = \"""
        ... <html>
        ... <head><style>
        ... #a { margin: 0 }
        ... .a { margin: 1em }
        ... span.b { padding: 0 }
        ... div.b { padding: 1em }
        ... @media screen { div.a { top: 0 }}
        ... .c { background: white url(text.gif) no-repeat fixed bottom left !important }
        ... .d { background: url(text.gif) repeat-x 2px -8px }
        ... #a span { display: block }
        ... .a span { display: none }
        ... </style></head>
        ... <body>
        ... <div id='a'>
        ...   <span class='b c'>test</span>
        ...   <div class='d'><!-- nothing here --></div>
        ...   <span>test</span>
        ... </div>
        ... </body>
        ... </html>\"""

        >>> out_1 = compactify(text, filter_tags=False)
        >>> print(out_1)
        <BLANKLINE>
        <html>
        <head></head>
        <body>
        <div id=\"a\" style=\"margin: 0\">
        <span class=\"b c\"...
        <div class=\"d\"...
        <span style=\"display: block\">test</span>
        </div>
        </body>
        </html>

        >>> import lxml.html

        Checking styles with non-deterministic order.

        >>> tree_1 = lxml.html.fromstring(out_1)

        Check 1: <span class=\"b c\" style=\"padding: 0; background-color: white !important; background-image: url(text.gif) !important; background-repeat: no-repeat !important; background-attachment: fixed !important; background-position: bottom left !important; display: block\">test</span>

        >>> el_1 = tree_1.xpath("//*[contains(@class, 'b')]")[0]
        >>> style_1 = el_1.attrib['style']
        >>> assert('padding: 0' in style_1)
        >>> assert('background-color: white !important' in style_1)
        >>> assert('background-image: url(text.gif) !important' in style_1)
        >>> assert('background-repeat: no-repeat !important' in style_1)
        >>> assert('background-attachment: fixed !important' in style_1)
        >>> assert('background-position: bottom left !important' in style_1)
        >>> assert('display: block' in style_1)

        Check 2: <div class=\"d\" style=\"background-image: url(text.gif); background-repeat: repeat-x; background-position: 2px -8px\"><!-- nothing here --></div>

        >>> el_2 = tree_1.xpath("//*[contains(@class, 'd')]")[0]
        >>> style_2 = el_2.attrib['style']
        >>> assert('background-image: url(text.gif)' in style_2)
        >>> assert('background-repeat: repeat-x' in style_2)
        >>> assert('background-position: 2px -8px' in style_2)


        Compactify with different options

        >>> out_2 = compactify(text, filter_tags=False, remove_classnames_and_ids=True)
        >>> print(out_2)
        <BLANKLINE>
        <html>
        <head></head>
        <body>
        <div style=\"margin: 0\">
        <span ...
        <div ...
        <span style=\"display: block\">test</span>
        </div>
        </body>
        </html>

        """

        # save arguments
        self.filter_tags = filter_tags
        self.expand_css_properties = expand_css_properties
        self.media = media

        self.classes = {}
        self.identifiers = {}

        # optimize class identifiers
        count = 0
        for tag in self.find_all():
            class_def = tag.get("class", None)
            id_def = tag.get("id", None)
            if class_def:
                # convert class-identifiers to abbreviated versions
                short_names = []
                for c in class_def:
                    name = c.strip()
                    short_name = self.classes.get(
                        name, "%s%s" % (self.class_prefix, count)
                    )
                    if not name in self.classes:
                        # store abbr. identifier in dictionary
                        self.classes[name] = short_name
                        count += 1

                        short_names.append(short_name)

                if abbreviation_enabled:
                    tag["class"] = " ".join(short_names)

            if id_def:
                # convert class-identifiers to abbreviated versions
                short_names = []
                for c in id_def.split(" "):
                    name = c.strip()
                    short_name = self.identifiers.get(
                        name, "%s%s" % (self.id_prefix, count)
                    )
                    if not name in self.identifiers:
                        # store abbr. identifier in dictionary
                        self.identifiers[name] = short_name
                        count += 1

                    short_names.append(short_name)

                if abbreviation_enabled:
                    tag["id"] = " ".join(short_names)

        style_defs = self.find_all("style")
        for style_def in style_defs:
            # assert non-empty
            if not style_def.contents:
                continue

            style = style_def.contents[0]

            # remove unused rules
            sheet = cssutils.parseString(style)

            ### INFO: workaround of bug:
            ### http://code.google.com/p/cssutils/issues/detail?id=39
            ### TODO: after bugfix restore to easier to read:
            # sheet.cssRules = self.filterCSSDeclarations(sheet.cssRules)
            filtered_cssrules = self.filterCSSDeclarations(sheet.cssRules)
            del sheet.cssRules[:]
            for fcss in filtered_cssrules:
                sheet.cssRules.append(fcss)
            style = safe_text(sheet.cssText)

            # convert identifiers
            if abbreviation_enabled:
                for name, short_name in self.classes.items():
                    style = style.replace(".%s " % name, ".%s " % short_name)
                    style = style.replace(".%s." % name, ".%s." % short_name)
                    style = style.replace(".%s," % name, ".%s," % short_name)

                for name, short_name in self.identifiers.items():
                    style = style.replace("#%s " % name, "#%s " % short_name)
                    style = style.replace("#%s." % name, "#%s." % short_name)
                    style = style.replace("#%s," % name, "#%s," % short_name)

            style_def.contents[0].replace_with(style)

            if styles_in_tags:
                # distribute styles
                for rule in sheet.cssRules:
                    self.distributeCSSDeclaration(rule)

                # remove class names and identifiers from tags
                if remove_classnames_and_ids:
                    for tag in self.find_all():
                        tag.attrs.pop("class", None)
                        tag.attrs.pop("id", None)

                # remove inline style-declarations
                style_def.extract()

        if IS_PY2:
            return self.encode_contents()
        return str(self)

    def distributeCSSDeclaration(self, rule):
        if isinstance(rule, cssutils.css.CSSComment):
            return
        elif isinstance(rule, cssutils.css.CSSMediaRule):
            # verify that media is valid
            valid_media = False
            for med in rule.media:
                mediatext = getattr(med, "mediaText", "")
                if mediatext in self.media or mediatext == "all":
                    valid_media = True
                    break

            if not valid_media:
                return

            for rul in rule.cssRules:
                self.distributeCSSDeclaration(rul)
        else:
            for selector in rule.selectorList:
                # create selector datastructure
                selectors = []
                for match in regex_selector.finditer(selector.selectorText):
                    if not match.group(0):
                        continue

                    selectors.append(
                        (
                            match.group(1),
                            trim_dictionary(
                                {"class": match.group(5), "id": match.group(3)}
                            ),
                        )
                    )

                # distribute selector to document
                self.distributeCSSRule(rule, self, selectors)

    def expandProperty(self, style, prop):
        value = style.getPropertyValue(prop)
        important = style.getPropertyPriority(prop)

        style.removeProperty(prop)

        # handle properties
        regex = regex_tags[prop]
        match = regex.match(value)

        if match:
            for p, v in match.groupdict().items():
                aggregate_property = "-".join((prop, p))
                if v is not None:
                    style.setProperty(aggregate_property, v, priority=important)
        else:
            style.setProperty(prop, value)

    def distributeCSSRule(self, rule, basetag, selectors):
        tag_name, attrs = selectors[0]
        tags = basetag.find_all(lambda tag: tagQuery(tag, tag_name, attrs))

        # walk down all matching paths
        for tag in tags:
            if len(selectors) > 1:
                # continue matching down this path
                self.distributeCSSRule(rule, tag, selectors[1:])
            else:
                # expand properties
                if self.expand_css_properties:
                    i = 0
                    while i < rule.style.length:
                        prop = rule.style.item(i)

                        # check if property is in expand list
                        if prop in regex_tags:
                            self.expandProperty(rule.style, prop)

                        i += 1

                # filter out blacklisted properties
                if self.filter_tags:
                    i = 0
                    while i < rule.style.length:
                        prop = rule.style.item(i)

                        # check if property is in blacklist
                        if prop in tag_blacklist:
                            rule.style.removeProperty(prop)
                        else:
                            i += 1

                # format style-declaration
                style = rule.style.cssText.replace("\n", " ").strip(" \n\r")
                while "  " in style:
                    style = style.replace("  ", " ")

                # apply to tags
                attrs = tag.attrs
                style_key = ""
                for key in attrs:
                    if key.lower() == "style":
                        style_key = key
                        break

                if style_key:
                    attrs[style_key] = "%s; %s" % (attrs[style_key], style)
                    style = None

                if style:
                    attrs["style"] = style

    def filterCSSDeclarations(self, cssRules):
        rules = []
        for rule in cssRules:
            if isinstance(rule, cssutils.css.CSSComment):
                continue

            if isinstance(rule, cssutils.css.CSSMediaRule):
                filtered_rules = self.filterCSSDeclarations(rule.cssRules)

                # api requires explicit removal
                i = 0
                while i < len(rule.cssRules):
                    r = rule.cssRules[i]
                    if r not in filtered_rules:
                        rule.deleteRule(i)
                    else:
                        i += 1

                rules.append(rule)
                continue

            # only include rules with at least one used selector
            try:
                selector_list = self.filterCSSDeclaration(rule)
            except:
                continue

            if len(selector_list):
                rule.selectorList = selector_list
                rules.append(rule)

        return rules

    def filterCSSDeclaration(self, rule):
        selector_list = cssutils.css.selectorlist.SelectorList()
        for selector in rule.selectorList:
            # remove unused selectors
            iterator = regex_selector_id.finditer(selector.selectorText)

            add = True
            for match in iterator:
                s = match.group(1)
                if s.startswith(".") and s[1:] not in self.classes:
                    add = False
                    break
                elif s.startswith("#") and s[1:] not in self.identifiers:
                    add = False
                    break

            if add:
                selector_list.appendSelector(selector.selectorText)
        return selector_list


def _test():
    import doctest

    doctest.testmod(
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE, raise_on_error=True
    )


if __name__ == "__main__":
    _test()
