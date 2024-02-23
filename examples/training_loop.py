import logging
from statistics import NormalDist
from time import sleep

from progress_api.api import make_progress

EPOCHS = 5
BATCHES = 100

_log = logging.getLogger(__name__)


def main():
    time = NormalDist(5)
    adjust = NormalDist(-0.05, 0.05)

    loss = NormalDist(0.9, 0.1).samples(1)[0]

    with make_progress(_log, "epochs", EPOCHS) as epochs:
        for epoch in range(EPOCHS):
            _log.info("beginning epoch %d", epoch + 1)
            batches = make_progress(_log, "batches", BATCHES)
            for batch in range(BATCHES):
                _log.debug("training batch %d", batch)
                delay = time.samples(1)[0]
                sleep(delay * delay / 1000)
                loss += adjust.samples(1)[0]
                batches.set_metric("loss", loss, "{:.3f}")
                batches.update(1)
            batches.finish()
            epochs.update(1)
        epochs.finish()


if __name__ == "__main__":
    main()
