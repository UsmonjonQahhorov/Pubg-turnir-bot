from bot.dispatcher import dp
from .check_sub import BigBrother
from .throttling import ThrottlingMiddleware

if __name__ == 'middlewares':
    dp.middleware.setup(BigBrother())
    dp.middleware.setup(ThrottlingMiddleware())
