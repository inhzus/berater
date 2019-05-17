# -*- coding: utf-8 -*-
# created by inhzus

from typing import List

from bert_serving.client import BertClient

client = BertClient(ip='ali.zsuun.com', port=8002, port_out=8003)


def candidate_answer(q: str) -> List[List]:
    answer = client.encode([q])
    return answer


if __name__ == '__main__':
    print(candidate_answer('南大'))
