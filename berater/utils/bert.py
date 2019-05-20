# -*- coding: utf-8 -*-
# created by inhzus

from typing import List

from bert_serving.client import BertClient


def candidate_answer(q: str) -> List[List]:
    try:
        with BertClient(ip='ali.zsuun.com', port=8002, port_out=8003, timeout=3000) as client:
            answer = client.encode([q])
    except TimeoutError:
        answer = None
    return answer


if __name__ == '__main__':
    print(candidate_answer('南大'))
