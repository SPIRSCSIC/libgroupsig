/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

#include "bld_key_handles.h"
#include "key.h"
#include "logger.h"

const bld_key_handle_t* groupsig_bld_key_handle_from_code(uint8_t code) {

  int i;

  for(i=0; i<GROUPSIG_BLD_KEY_HANDLES_N; i++) {
    if(GROUPSIG_BLD_KEY_HANDLES[i]->code == code)
      return GROUPSIG_BLD_KEY_HANDLES[i];
  }

  return NULL;

}

groupsig_key_t* groupsig_bld_key_init(uint8_t code) {

  const bld_key_handle_t *gkh;

  if(!(gkh = groupsig_bld_key_handle_from_code(code))) {
    return NULL;
  }

  return gkh->init();

}

int groupsig_bld_key_free(groupsig_key_t *key) {

  const bld_key_handle_t *gkh;

  if(!key) {
    LOG_EINVAL_MSG(&logger, __FILE__, "groupsig_bld_key_free", __LINE__,
		   "Nothing to free.", LOGWARN);
    return IOK;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return IERROR;
  }

  gkh->free(key);

  return IOK;

}

groupsig_key_t* groupsig_bld_key_random(uint8_t code, void *param) {

  const bld_key_handle_t *gkh;

  if(!(gkh = groupsig_bld_key_handle_from_code(code))) {
    return NULL;
  }

  return gkh->random(param);

}

int groupsig_bld_key_copy(groupsig_key_t *dst, groupsig_key_t *src) {

  const bld_key_handle_t *gkh;

  if(!dst || !src ||
     dst->scheme != src->scheme) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_copy", __LINE__, LOGERROR);
    return IERROR;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(dst->scheme))) {
    return IERROR;
  }

  return gkh->copy(dst, src);

}

int groupsig_bld_key_get_size(groupsig_key_t *key) {

  const bld_key_handle_t *gkh;

  if(!key) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_get_size",
	       __LINE__, LOGERROR);
    return IERROR;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return IERROR;
  }

  return gkh->get_size(key);

}

int groupsig_bld_key_export(byte_t **dst,
			    uint32_t *size,
			    groupsig_key_t *key) {

  const bld_key_handle_t *gkh;

  if(!dst || !size || !key) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_export",
	       __LINE__, LOGERROR);
    return IERROR;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return IERROR;
  }

  return gkh->gexport(dst, size, key);

}

int groupsig_bld_key_export_pub(byte_t **dst,
				uint32_t *size,
				groupsig_key_t *key) {

  const bld_key_handle_t *gkh;

  if(!dst || !size || !key) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_export_pub",
	       __LINE__, LOGERROR);
    return IERROR;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return IERROR;
  }

  return gkh->gexport_pub(dst, size, key);

}

int groupsig_bld_key_pub(groupsig_key_t *key, groupsig_key_t **pub) {

  const bld_key_handle_t *gkh;

  if(!key) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_pub",
	       __LINE__, LOGERROR);
    return IERROR;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return IERROR;
  }

  return gkh->pub(key, pub);

}

int groupsig_bld_key_export_prv(byte_t **dst,
				uint32_t *size,
				groupsig_key_t *key) {

  const bld_key_handle_t *gkh;

  if(!dst || !size || !key) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_export_prv", __LINE__, LOGERROR);
    return IERROR;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return IERROR;
  }

  return gkh->gexport_prv(dst, size, key);

}

int groupsig_bld_key_prv(groupsig_key_t *key, groupsig_key_t **prv) {

  const bld_key_handle_t *gkh;

  if(!key) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_prv",
	       __LINE__, LOGERROR);
    return IERROR;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return IERROR;
  }

  return gkh->prv(key, prv);

}

groupsig_key_t* groupsig_bld_key_import(uint8_t code,
					byte_t *source,
					uint32_t size) {

  const bld_key_handle_t *gkh;

  if(!source) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_import", __LINE__, LOGERROR);
    return NULL;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(code))) {
    return NULL;
  }

  return gkh->gimport(source, size);

}

char* groupsig_bld_key_to_string(groupsig_key_t *key) {

  const bld_key_handle_t *gkh;

  if(!key) {
    LOG_EINVAL(&logger, __FILE__, "groupsig_bld_key_to_string", __LINE__, LOGERROR);
    return NULL;
  }

  if(!(gkh = groupsig_bld_key_handle_from_code(key->scheme))) {
    return NULL;
  }

  return gkh->to_string(key);

}

/* bld_key.c ends here */
