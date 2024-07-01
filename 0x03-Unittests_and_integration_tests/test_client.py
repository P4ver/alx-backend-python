#!/usr/bin/env python3
""" Unit and Integration Tests for GithubOrgClient """

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock


class TestGithubOrgClient(unittest.TestCase):
    """ Unit tests for GithubOrgClient """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test the org method in GithubOrgClient"""
        client_instance = GithubOrgClient(org_name)
        client_instance.org()
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}'
        )

    def test_public_repos_url(self):
        """ Test the _public_repos_url property in GithubOrgClient """
        ac = 'client.GithubOrgClient.org'
        with patch(ac, new_callable=PropertyMock) as m_org:
            payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
            m_org.return_value = payload
            client_instance = GithubOrgClient('test')
            result = client_instance._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method in GithubOrgClient.
        Verify the list of repos matches the expected payload.
        Check that the mocked property and get_json are called once.
        """
        json_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_get_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/test/repos"
            )
            client_instance = GithubOrgClient('test')
            result = client_instance.public_repos()

            expected_result = [repo["name"] for repo in json_payload]
            self.assertEqual(result, expected_result)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """ Unit test for has_license method in GithubOrgClient """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration tests for GithubOrgClient using fixtures """

    @classmethod
    def setUpClass(cls):
        """Setup method called before tests in the class"""
        config = {
            'return_value.json.side_effect': [
                cls.org_payload, cls.repos_payload,
                cls.org_payload, cls.repos_payload
            ]
        }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock_get = cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration test for public_repos method in GithubOrgClient """
        client_inst = GithubOrgClient("google")

        self.assertEqual(client_inst.org, self.org_payload)
        self.assertEqual(client_inst.repos_payload, self.repos_payload)
        self.assertEqual(client_inst.public_repos(), self.expected_repos)
        self.assertEqual(client_inst.public_repos("non_existent_license"), [])
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """ Integration test for public_repos method with license filter in
        GithubOrgClient """
        client_inst = GithubOrgClient("google")

        self.assertEqual(client_inst.public_repos(), self.expected_repos)
        self.assertEqual(client_inst.public_repos("non_existent_license"), [])
        self.assertEqual(
            client_instance.public_repos("apache-2.0"),
            self.apache2_repos
        )
        self.mock_get.assert_called()

    @classmethod
    def tearDownClass(cls):
        """Teardown method called after tests in the class"""
        cls.get_patcher.stop()
