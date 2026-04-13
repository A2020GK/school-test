/**
 * Flask Session Cookie Encoder
 *
 * Reproduces the itsdangerous + Flask SecureCookieSessionInterface signing
 * algorithm in pure JavaScript (Web Crypto API) for local testing purposes.
 *
 * Algorithm (matches Flask 3.x / itsdangerous 2.x):
 *   1. Serialize the payload as compact JSON.
 *      (TaggedJSONSerializer is identical to compact JSON for plain
 *       dicts/strings/numbers/booleans — no special type tags needed.)
 *   2. Base64url-encode the JSON bytes (no padding).
 *   3. Encode the current Unix timestamp as a minimal big-endian byte
 *      sequence and base64url-encode it (no padding).
 *   4. Derive the signing key:
 *        derived_key = HMAC-SHA1(key=secret_key, msg="cookie-session")
 *   5. Compute the signature:
 *        sig = HMAC-SHA1(key=derived_key, msg=data_b64 + "." + ts_b64)
 *   6. Base64url-encode the signature (no padding).
 *   7. Return:  data_b64 + "." + ts_b64 + "." + sig_b64
 *
 * Usage:
 *   const cookie = await encodeFlaskSession({ logged_in: true }, 'local-test-secret');
 *   document.cookie = `session=${cookie}; path=/`;
 *
 * ⚠️  FOR LOCAL TESTING ONLY — never expose a real secret key on the frontend.
 */

/**
 * Encode a JavaScript value as base64url without padding.
 * @param {Uint8Array} bytes
 * @returns {string}
 */
function base64urlEncode(bytes) {
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}

/**
 * Convert a non-negative integer to its minimal big-endian byte representation
 * (leading zero bytes stripped), matching itsdangerous' int_to_bytes().
 * @param {number} num
 * @returns {Uint8Array}
 */
function intToBytes(num) {
  if (num === 0) return new Uint8Array([0]);
  const bytes = [];
  while (num > 0) {
    bytes.unshift(num & 0xff);
    num = Math.floor(num / 256);
  }
  return new Uint8Array(bytes);
}

/**
 * Compute HMAC-SHA1 and return the raw digest bytes.
 * @param {Uint8Array|ArrayBuffer} keyBytes
 * @param {Uint8Array|ArrayBuffer} msgBytes
 * @returns {Promise<Uint8Array>}
 */
async function hmacSha1(keyBytes, msgBytes) {
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyBytes,
    { name: 'HMAC', hash: 'SHA-1' },
    false,
    ['sign']
  );
  const signature = await crypto.subtle.sign('HMAC', cryptoKey, msgBytes);
  return new Uint8Array(signature);
}

/**
 * Encode a payload dict as a signed Flask session cookie value.
 *
 * The result can be set directly as the "session" cookie that Flask will
 * accept and decode into `flask.session` on the server side.
 *
 * @param {Object} payload      - Plain-object session data (e.g. { logged_in: true }).
 * @param {string} secretKey    - The Flask app.secret_key value.
 * @returns {Promise<string>}   - The signed cookie string.
 *
 * @example
 * const cookie = await encodeFlaskSession({ logged_in: true }, 'local-test-secret');
 * document.cookie = `session=${cookie}; path=/; SameSite=Lax`;
 */
async function encodeFlaskSession(payload, secretKey) {
  const enc = new TextEncoder();

  // Step 1 & 2 — serialize and base64url-encode the payload
  const jsonBytes = enc.encode(JSON.stringify(payload));
  const dataB64 = base64urlEncode(jsonBytes);

  // Step 3 — timestamp: raw Unix seconds (itsdangerous 2.x uses time.time() directly)
  const timestamp = Math.floor(Date.now() / 1000);
  const tsB64 = base64urlEncode(intToBytes(timestamp));

  // Step 4 — derive the signing key: HMAC-SHA1(secret_key, "cookie-session")
  const derivedKey = await hmacSha1(enc.encode(secretKey), enc.encode('cookie-session'));

  // Step 5 & 6 — sign and base64url-encode the signature
  const valueToSign = enc.encode(dataB64 + '.' + tsB64);
  const sigBytes = await hmacSha1(derivedKey, valueToSign);
  const sigB64 = base64urlEncode(sigBytes);

  return `${dataB64}.${tsB64}.${sigB64}`;
}

/**
 * Convenience helper: encode the payload and write it to document.cookie.
 *
 * @param {Object} payload   - Session payload (e.g. { logged_in: true }).
 * @param {string} secretKey - Flask app.secret_key.
 * @param {string} [path='/'] - Cookie path.
 */
async function setFlaskSessionCookie(payload, secretKey, path = '/') {
  const cookieValue = await encodeFlaskSession(payload, secretKey);
  document.cookie = `session=${cookieValue}; path=${path}; SameSite=Lax`;
  return cookieValue;
}
