#!/usr/bin/env python3
"""CreateRedirectBot: Create redirect page in page-target pair, single or in batch.

-summary:   The text used as edit summary, automatically filled when not set.
-page:      The title of the new redirection page.
-target:    The title of page that the new redirection page pointed to.
-pairsfile: The file indicates redirection page names and its targets in batch creation, in format:
    redr_page1
    redr_target1
    ...
-force      Create it, whether it was already existed, will overwrite the existing contents.
-nolocale   Disable localization on redirect link, use "#REDIRECT" instead.

NOTE: If both "page"-"target" pair and "pairsfile" are set, the last "page"-"target" pair will also be processed."""
#
# (C) Bilin Tsui, 2024
#
# Distributed under the terms of the MIT license.
#
import pywikibot
from pywikibot import i18n, pagegenerators
from pywikibot.bot import SingleSiteBot
from itertools import zip_longest

class CreateRedirectBot( SingleSiteBot ):
    update_options = {
            'summary': '',
            'page': '',
            'target': '',
            'pairsfile': '',
            'force': False,
            'nolocale': False,
    }

    def create_one( self, page, target ) -> None:
        if self.opt.force != True and page.exists():
            pywikibot.warning( i18n.twtranslate( page.site, 'create_redirect-page-existed' ).format( page = page ) )
            return True
        options = {}
        options[ 'summary' ] = self.opt.summary
        if options[ 'summary' ] == '':
            options[ 'summary' ] = i18n.twtranslate( page.site, 'create_redirect-defaultsummary', { 'target': target } )

        text = ''
        if self.opt.nolocale == True:
            text = '#REDIRECT [[' + target + ']]'
        else:
            text = i18n.twtranslate( page.site, 'create_redirect-linkformat', { 'target': target } )
        self.userPut( page, page.text, text, **options )

def main( *args: str ) -> None:
    options = {}
    from_to_pairs = []
    local_args = pywikibot.handle_args( args )

    for arg in local_args:
        arg, _, value = arg.partition( ':' )
        option = arg[ 1: ]
        if option in ( 'summary', 'page', 'target'):
            options[ option ] = value or pywikibot.input( i18n.twtranslate( page.site, 'create_redirect-missing-arg-prompt', { 'arg': option } ) )
        elif option == 'pairsfile':
            filename = value or pywikibot.input( i18n.twtranslate( page.site, 'create_redirect-missing-arg-prompt', { 'arg': option } ) )
            page_gen = [ pagegenerators.TextIOPageGenerator( filename ) ] * 2
            for page, target in zip_longest( *page_gen, fillvalue = None ):
                if target is None:
                    pywikibot.warning( i18n.twtranslate( page.site, 'create_redirect-pairsfile-odd-num', { 'filename': filename }) )
                else:
                    from_to_pairs.append( [ page.title(), target.title()])
            options[ option ] = value
        else:
            options[ option ] = True

    if 'page' in options and 'target' in options:
        from_to_pairs.append( [ options[ 'page' ], options[ 'target' ] ] )

    site = pywikibot.Site()
    if not site.logged_in():
        site.login()
    bot = CreateRedirectBot( **options )
    for page, target in from_to_pairs:
        bot.create_one( pywikibot.Page( site, page ), target )

if __name__ == '__main__':
    main()
