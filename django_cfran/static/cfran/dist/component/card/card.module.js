/*! CFRAN v11.2.1 | SPDX-License-Identifier: MIT | License-Filename: LICENSE.md | restricted use (see terms and conditions) */

const config = {
  prefix: 'cfran',
  namespace: 'cfran',
  version: '11.2.1'
};

const api = window[config.namespace];

class CardDownload extends api.core.Instance {
  static get instanceClassName () {
    return 'CardDownload';
  }

  init () {
    this.addAscent(api.core.AssessEmission.UPDATE, details => {
      this.descend(api.core.AssessEmission.UPDATE, details);
    });
    this.addAscent(api.core.AssessEmission.ADDED, () => {
      this.descend(api.core.AssessEmission.ADDED);
    });
  }
}

const CardSelector = {
  DOWNLOAD: api.internals.ns.selector('card--download'),
  DOWNLOAD_DETAIL: `${api.internals.ns.selector('card--download')} ${api.internals.ns.selector('card__end')} ${api.internals.ns.selector('card__detail')}`
};

api.card = {
  CardSelector: CardSelector,
  CardDownload: CardDownload
};

api.internals.register(api.card.CardSelector.DOWNLOAD, api.card.CardDownload);
api.internals.register(api.card.CardSelector.DOWNLOAD_DETAIL, api.core.AssessDetail);
//# sourceMappingURL=card.module.js.map