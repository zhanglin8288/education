from __future__ import unicode_literals

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed
from django.utils.html import strip_tags

from mezzanine.core.templatetags.mezzanine_tags import richtext_filters
from .models import NewsPost, NewsCategory
from mezzanine.generic.models import Keyword
from mezzanine.pages.models import Page
from mezzanine.conf import settings
from mezzanine.utils.models import get_user_model


User = get_user_model()


class PostsRSS(Feed):
    """
    RSS feed for all news posts.
    """

    def __init__(self, *args, **kwargs):
        """
        Use the title and description of the News page for the feed's
        title and description. If the news page has somehow been
        removed, fall back to the ``SITE_TITLE`` and ``SITE_TAGLINE``
        settings.
        """
        self.tag = kwargs.pop("tag", None)
        self.category = kwargs.pop("category", None)
        self.username = kwargs.pop("username", None)
        super(PostsRSS, self).__init__(*args, **kwargs)
        self._public = True
        try:
            page = Page.objects.published().get(slug=settings.NEWS_SLUG)
        except Page.DoesNotExist:
            page = None
        else:
            self._public = not page.login_required
        if self._public:
            settings.use_editable()
            if page is not None:
                self._title = "%s | %s" % (page.title, settings.SITE_TITLE)
                self._description = strip_tags(page.description)
            else:
                self._title = settings.SITE_TITLE
                self._description = settings.SITE_TAGLINE

    def title(self):
        return self._title

    def description(self):
        return self._description

    def link(self):
        return reverse("news_post_list")

    def items(self):
        if not self._public:
            return []
        news_posts = NewsPost.objects.published().select_related("user")
        if self.tag:
            tag = get_object_or_404(Keyword, slug=self.tag)
            news_posts = news_posts.filter(keywords__keyword=tag)
        if self.category:
            category = get_object_or_404(NewsCategory, slug=self.category)
            news_posts = news_posts.filter(categories=category)
        if self.username:
            author = get_object_or_404(User, username=self.username)
            news_posts = news_posts.filter(user=author)
        limit = settings.NEWS_RSS_LIMIT
        if limit is not None:
            news_posts = news_posts[:settings.NEWS_RSS_LIMIT]
        return news_posts

    def item_description(self, item):
        return richtext_filters(item.content)

    def categories(self):
        if not self._public:
            return []
        return NewsCategory.objects.all()

    def item_author_name(self, item):
        return item.user.get_full_name() or item.user.username

    def item_author_link(self, item):
        username = item.user.username
        return reverse("news_post_list_author", kwargs={"username": username})

    def item_pubdate(self, item):
        return item.publish_date

    def item_categories(self, item):
        return item.categories.all()


class PostsAtom(PostsRSS):
    """
    Atom feed for all news posts.
    """

    feed_type = Atom1Feed

    def subtitle(self):
        return self.description()
