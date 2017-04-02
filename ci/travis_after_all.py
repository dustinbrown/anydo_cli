import json

import os
import time
import logging
from typing import List

import requests

log = logging.getLogger("travis.leader")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)


class MatrixElement(object):

    def __init__(self, json_raw):
        self.is_finished = json_raw['finished_at'] is not None
        self.is_succeeded = json_raw['result'] == 0
        self.number = json_raw['number']


class TravisAfterAll:
    """
    This requires a build matrix(ie, more than one build). This will break for single builds as
    'TRAVIS_JOB_NUMBER' will not exist
    """
    TRAVIS_ENTRY = 'https://api.travis-ci.org'

    def __init__(self):
        self.job_number = os.getenv('TRAVIS_JOB_NUMBER')
        self.build_id = os.getenv('TRAVIS_BUILD_ID')
        self.polling_interval = int(os.getenv('POLLING_INTERVAL', '5'))
        gh_token = os.getenv('GITHUB_TOKEN')
        self.travis_token = TravisAfterAll.get_travis_token(gh_token)

        if not self.is_leader():
            log.info("Not the leader, no reason for me to be running. Exiting..")
            raise SystemExit

    def can_publish(self):
        return self.is_leader() and self.others_are_successful()

    def is_leader(self):
        """
        leader is the last build number to start
        """
        matrix_job = self.get_matrix_snapshot()[-1]
        return self.job_number == matrix_job.number

    def get_matrix_snapshot(self) -> List[MatrixElement]:
        """
        :return: Matrix List
        """
        headers = {'content-type': 'application/json',
                   'Authorization': 'token {}'.format(self.travis_token)}
        req = requests.get("{0}/builds/{1}".format(TravisAfterAll.TRAVIS_ENTRY, self.build_id),
                           headers=headers)
        raw_json = req.json()
        return [MatrixElement(job) for job in raw_json["matrix"]]

    @staticmethod
    def get_travis_token(gh_token: str) -> str:
        data = {"github_token": gh_token}
        headers = {'content-type': 'application/json', 'User-Agent': 'Travis/1.0'}

        req = requests.post("{0}/auth/github".format(TravisAfterAll.TRAVIS_ENTRY),
                            data=json.dumps(data), headers=headers)

        travis_token = req.json().get('access_token')

        return travis_token

    def others_are_successful(self) -> bool:
        try:
            final_snapshot = self.wait_for_all_builds_finish()
            all_successful = all(job.is_succeeded for job in final_snapshot)
            if not all_successful:
                log.warning("Final Results: {0}".format(
                    [(job.number, job.is_succeeded) for job in final_snapshot])
                )
            return all_successful
        except Exception as e:
            log.error("Unable to wait fo all builds to finish", e)
            return False

    def wait_for_all_builds_finish(self) -> List[MatrixElement]:
        job_list = []
        finished = False
        while not finished:
            job_list = [job for job in self.get_matrix_snapshot() if job.number != self.job_number]
            finished = all(job.is_finished for job in job_list)
            time.sleep(self.polling_interval)
            log.info("Waiting for other builds to finish...")

        return job_list

if __name__ == '__main__':
    pass

