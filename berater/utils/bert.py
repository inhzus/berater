# -*- coding: utf-8 -*-
# created by inhzus

from typing import List

from bert_serving.client import BertClient


def candidate_answer(q: str) -> List[List]:
    try:
        with BertClient(ip='weixinbak.njunova.com', port=32012, port_out=32013, timeout=3000) as client:
            answer = client.encode([q])
    except TimeoutError:
        answer = None
    return answer


if __name__ == '__main__':
    print(candidate_answer('南大'))
