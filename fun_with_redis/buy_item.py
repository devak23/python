import logging as log

import redis

log.basicConfig()


class OutOfStockError(Exception):
    'Raised when out of stock situation is reached'


def buyitem(r: redis.Redis, itemid: int) -> None:
    with r.pipeline() as pipe:
        error_count = 0
        while True:
            try:
                # get available inventory, watching for changes related to this itemid before the transaction
                pipe.watch(itemid)
                nleft:bytes = r.hget(itemid, 'quantity')
                if nleft > b"0":
                    pipe.multi()
                    pipe.hincrby(itemid, 'quantity', -1)
                    pipe.hincrby(itemid, 'npurchased', 1)
                    pipe.execute()
                    break
                else:
                    # stop watching the itemid and raise to break out
                    pipe.unwatch()
                    raise OutOfStockError(f'Sorry, {itemid} is out of stock!')
            except redis.WatchError:
                # Log total num of errors by this user to buy this item then try the same process again of
                # WATCH/HGET/MULTI/EXEC
                error_count += 1
                log.warning('Watch Error #%d: %s; retrying', error_count, itemid)

    return None


if __name__ == '__main__':
    r = redis.Redis()
    buyitem(r, 'inventory:11934279')
    buyitem(r, 'inventory:11934279')
    buyitem(r, 'inventory:11934279')
    print(r.hmget('inventory:11934279', 'quantity', 'npurchased'))
