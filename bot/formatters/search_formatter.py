from html import escape

from bot.models.search_result import SearchResult


def format_wikipedia_result(article: SearchResult) -> str:
    item = f"<b>{escape(article.title)}</b>"

    if article.description:
        item += f"\n{escape(article.description)}"

    return (
        f"{item} \n"
        f'<a href="{escape(article.url, quote=True)}">'
        f"🔗 Читать статью</a>"
    )


def format_github_result(article: SearchResult) -> str:
    item = f"<b>{escape(article.title)}</b>"

    if article.description:
        item += f"\n{escape(article.description)}"

    if article.stars is not None:
        item += f"\n⭐ {escape(str(article.stars))}"

    if article.language is not None:
        item += f" • 💻 {escape(article.language)}"

    item += (
        f' • <a href="{escape(article.url, quote=True)}">'
        f"🔗 Открыть репозиторий</a>"
    )

    return item


def format_stackoverflow_result(article: SearchResult) -> str:
    item = f"<b>{escape(article.title)}</b>"

    if article.score is not None:
        item += f"\n👍 Рейтинг: {escape(str(article.score))}"

    if article.answers is not None:
        item += f" • 💬 Ответы: {escape(str(article.answers))}"

    if article.status is not None:
        item += f" • ✅ {escape(article.status)}"

    item += (
        f'\n<a href="{escape(article.url, quote=True)}">'
        f"🔗 Открыть вопрос</a>"
    )

    return item


def format_search_results(results: list[SearchResult]) -> str:
    groups = {
        "Wikipedia": [],
        "GitHub": [],
        "StackOverflow": [],
    }

    formatters = {
        "Wikipedia": format_wikipedia_result,
        "GitHub": format_github_result,
        "StackOverflow": format_stackoverflow_result,
    }

    for article in results:
        if article.source in groups:
            formatted = formatters[article.source](article)
            groups[article.source].append(formatted)

    sections = ["<b>🔎 Результаты поиска</b>"]

    titles = {
        "Wikipedia": "📚 Википедия",
        "GitHub": "💻 GitHub",
        "StackOverflow": "❓ Stack Overflow",
    }

    for source, articles in groups.items():
        if articles:
            section = f"─────── <b>{titles[source]}</b> ───────\n\n"
            section += "\n\n".join(articles)
            sections.append(section)

    return "\n\n".join(sections)
