#!/bin/bash

# RSS Listing
i18ndude rebuild-pot --pot jyu/rsslisting/locales/jyu.rsslisting.pot --create jyu.rsslisting jyu/rsslisting
i18ndude sync --pot jyu/rsslisting/locales/jyu.rsslisting.pot jyu/rsslisting/locales/*/LC_MESSAGES/jyu.rsslisting.po

# Plone
i18ndude rebuild-pot --pot jyu/rsslisting/i18n/plone.pot --create plone jyu/rsslisting/profiles
i18ndude sync --pot jyu/rsslisting/i18n/plone.pot jyu/rsslisting/i18n/plone-*.po
