"""
Utility functions for search.

Functions
---------
:func:`advanced_search`: Provides advanced search functionality for Django models.

Revision History
----------------
* 2023-02-09: Created by @kms1212.
* 2023-02-18: Documented by @kms1212.
"""

import shlex
import datetime

from django.db.models import Q


def advanced_search(queryset, search):
    # pylint: disable=line-too-long
    """
    Provides advanced search functionality for Django models.

    Parameters / Return Values
    --------------------------

    :param queryset: The queryset to search.
    :param search: The search query.
    :returns: The filtered queryset.

    Description
    -----------

    Detailed description of the search query syntax:
    "search" argument is a string that contains keywords separated by spaces.
    Each spaces are treated as an AND operator.
    It is using shlex to parse the string, so whitespaces can be escaped by using backslash or quotation marks. (e.g. "hello world" or hello\\ world)
    Each keyword can be one of the following:

    .. list-table::
        :widths: 30 70
        :header-rows: 1

        * - Keyword
          - Description
        * - <keyword>
          - search for articles that contains <keyword> in the title.
        * - !<keyword>
          - search for exact match of <keyword> in the title.
        * - -<keyword>
          - exclude articles that contains <keyword> in the title.
        * - || or OR{case-insensive}
          - OR operator.
        * - :<key>=<value>
          - filter articles by <key> and <value>. ; Filter keys:
              * author: filter by author's username.
        * - @
          - date filter. ; Date filter syntax:
              * today: search for articles that are created today.
              * <date>: search for articles that are created on <date>.
              * > <date>: search for articles that are created after <date>.
              * < <date>: search for articles that are created before <date>.
              * <> <date1>~<date2>: search for articles that are created between <date1> and <date2>.
              * !<> <date1>~<date2>: search for articles that are created outside of <date1> and <date2>.

    Revision History
    ----------------
    * 2023-02-09: Created by @kms1212.
    """
    # pylint: enable=line-too-long

    def exact_match(keyword):
        return Q(title__iexact=keyword)

    def exclude(keyword):
        return ~Q(title__icontains=keyword)

    def filter_by(key, value):
        if key == 'author':
            return Q(author__username__iexact=value)
        return Q()

    def date_filter(keyword):
        if keyword == 'today':
            date1 = datetime.datetime.now().date()
            date2 = date1 + datetime.timedelta(days=1)
        elif keyword[0] == '>':
            try:
                date1 = datetime.datetime.strptime(keyword[1:], '%Y-%m-%d').date()
                date2 = date1 + datetime.timedelta(days=1)
            except ValueError:
                return Q()
        elif keyword[0] == '<':
            try:
                date1 = datetime.datetime.strptime(keyword[1:], '%Y-%m-%d').date()
                date2 = date1
                date1 = datetime.date(1970, 1, 1)
            except ValueError:
                return Q()
        elif keyword[1:3] == '<>':
            try:
                (date1, date2) = keyword[3:].split('~')
                date1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
                date2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()
                date2 += datetime.timedelta(days=1)
            except ValueError:
                return Q()
        else:
            return Q()
        return Q(created__range=(date1, date2))

    def contains(keyword):
        return Q(title__icontains=keyword)

    if search is not None and queryset.exists():
        search = shlex.split(search)
        qlist = [ Q() ]

        for keyword in search:
            if keyword.startswith('!'):
                # !: exact match
                qlist[len(qlist) - 1] &= exact_match(keyword[1:])

            elif keyword.startswith('-'):
                # -: exclude
                qlist[len(qlist) - 1] &= exclude(keyword[1:])

            elif keyword == '||' or keyword.lower() == 'or':
                # (||/or): OR
                qlist.append(Q())

            elif keyword.startswith(':'):
                # :<key>=<value>: filter
                (key, value) = keyword[1:].split('=')
                qlist[len(qlist) - 1] &= filter_by(key, value)

            elif keyword.startswith('@') and len(keyword) > 4:
                # @(</>/<>/!<>)<date>[~<date>]: date filter (YYYY-MM-DD)
                qlist[len(qlist) - 1] &= date_filter(keyword[1:])

            else:
                # <keyword>: search
                qlist[len(qlist) - 1] &= contains(keyword)

        qfilter = Q()

        for qcond in qlist:
            qfilter |= qcond

        queryset = queryset.filter(qfilter)


    return queryset
