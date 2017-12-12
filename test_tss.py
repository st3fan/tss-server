# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json, time
from pathlib import Path
from flask import url_for
import pytest

import tss

@pytest.fixture
def app(tmpdir):
    app = tss.app
    app.config["STORAGE_ROOT"] = str(tmpdir)
    return app

def test_hash_object_name():
    assert (tss.hash_object_name("hello.txt")) == "3857b672471862eab426eba0622e44bd2cedbd5d"
    assert (tss.hash_object_name("foo/bar.txt")) == "52235c6fb17f9b5c405adf27d35f65ce1ff388cb"

def test_mime_type_from_path():
    for extension, mime_type in tss.KNOWN_MIME_TYPES.items():
        assert tss.mime_type_from_path(Path("test." + extension)) == mime_type
    assert tss.mime_type_from_path(Path("test.unknown")) == tss.DEFAULT_MIME_TYPE

def test_make_object_path(tmpdir):
    path = tss.make_object_path(tmpdir, "test-bucket", "hello.txt", create=False)
    assert path == tmpdir + "/buckets/test-bucket/38/57/b672471862eab426eba0622e44bd2cedbd5d"
    assert path.exists() == False
    assert path.parent.exists() == False

def test_make_object_path_create(tmpdir):
    path = tss.make_object_path(tmpdir, "test-bucket", "hello.txt", create=True)
    assert path == tmpdir + "/buckets/test-bucket/38/57/b672471862eab426eba0622e44bd2cedbd5d"
    assert path.exists() == False
    assert path.parent.exists() == True

def test_make_bucket_path(tmpdir):
    path = tss.make_bucket_path(tmpdir, "test-bucket", create=False)
    assert path == tmpdir + "/buckets/test-bucket"
    assert path.exists() == False

def test_make_bucket_path_create(tmpdir):
    path = tss.make_bucket_path(tmpdir, "test-bucket", create=True)
    assert path == tmpdir + "/buckets/test-bucket"
    assert path.exists() == True
    # Creating a bucket that already exists should not throw any exceptions
    path = tss.make_bucket_path(tmpdir, "test-bucket", create=True)
    assert path == tmpdir + "/buckets/test-bucket"
    assert path.exists() == True



# def test_get_buckets(app, client):
#     res = client.get(url_for("get_buckets"))
#     assert res.status_code == 200
#     assert type(res.json) == list
#     assert len(res.json) == 0

#     res = client.put(url_for('put_object', bucket_name="foo", object_name="aaaaaaaaaaaaaaaaaaaaaaaa.txt"), data="test")
#     assert res.status_code == 200

#     res = client.get(url_for("get_buckets"))
#     assert res.status_code == 200
#     assert type(res.json) == list
#     assert len(res.json) == 1
#     assert "name" in res.json[0] and res.json[0]["name"] == "foo"
#     assert "created" in res.json[0]
#     assert "modified" in res.json[0]

#     res = client.put(url_for('put_object', bucket_name="bar", object_name="aaaaaaaaaaaaaaaaaaaaaaaa.txt"), data="test")
#     assert res.status_code == 200

#     res = client.get(url_for("get_buckets"))
#     assert res.status_code == 200
#     assert type(res.json) == list
#     assert len(res.json) == 2


# def test_authentication(app, client):

#     app.config["API_TOKEN"] = "85cf8bccd8a5b42e0a2c2f64a3645ba8c0a7d625"

#     # Put something without authentication
#     res = client.put(url_for('put_object', bucket_name="test_authentication", object_name="aaaaaaaaaaaaaaaaaaaaaaaa.txt"), data="test")
#     assert res.status_code == 401

#     # Put something with incorrect authentication
#     res = client.put(url_for('put_object', bucket_name="test_authentication", object_name="aaaaaaaaaaaaaaaaaaaaaaaa.txt"), data="test")
#     assert res.status_code == 401

#     # Put something with correct authentication
#     res = client.put(url_for('put_object', bucket_name="test_authentication", object_name="aaaaaaaaaaaaaaaaaaaaaaaa.txt"),
#                      data="test", headers={"Authorization": "token 85cf8bccd8a5b42e0a2c2f64a3645ba8c0a7d625"})
#     assert res.status_code == 200

