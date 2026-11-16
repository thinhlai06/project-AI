import 'dart:async';
import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

import 'package:mobile/core/api/health_check.dart';
import 'package:mobile/core/strings_vi.dart';

void main() {
  Uri base() => Uri.parse('http://10.0.2.2:8000');

  http.Response raw(String body, int status) =>
      http.Response.bytes(utf8.encode(body), status);

  http.Response obj(Object? value, int status) => raw(jsonEncode(value), status);

  group('checkHealth connected', () {
    test('ok true + version string -> connected with that version', () async {
      final client = MockClient((req) async =>
          obj({'ok': true, 'model_version': 'final-2026-11-08'}, 200));
      final result = await checkHealth(client, base());
      expect(result, isA<HealthConnected>());
      expect((result as HealthConnected).modelVersion, 'final-2026-11-08');
    });

    test('ok true + version null -> connected, version null', () async {
      final client =
          MockClient((req) async => obj({'ok': true, 'model_version': null}, 200));
      final result = await checkHealth(client, base());
      expect(result, isA<HealthConnected>());
      expect((result as HealthConnected).modelVersion, isNull);
    });

    test('ok true + version a number -> connected, version null', () async {
      final client =
          MockClient((req) async => obj({'ok': true, 'model_version': 7}, 200));
      final result = await checkHealth(client, base());
      expect(result, isA<HealthConnected>());
      expect((result as HealthConnected).modelVersion, isNull);
    });

    test('ok true + version missing -> connected, version null', () async {
      final client = MockClient((req) async => obj({'ok': true}, 200));
      final result = await checkHealth(client, base());
      expect(result, isA<HealthConnected>());
      expect((result as HealthConnected).modelVersion, isNull);
    });

    test('requests baseUri + /health', () async {
      Uri? seen;
      final client = MockClient((req) async {
        seen = req.url;
        return obj({'ok': true}, 200);
      });
      await checkHealth(client, base());
      expect(seen.toString(), 'http://10.0.2.2:8000/health');
    });

    test('Vietnamese diacritics in JSON are decoded as UTF-8', () async {
      final client = MockClient((req) async => raw(
          '{"ok":true,"model_version":"final-2026-11-08","note":"Đã sẵn sàng"}',
          200));
      final result = await checkHealth(client, base());
      expect(result, isA<HealthConnected>());
      expect((result as HealthConnected).modelVersion, 'final-2026-11-08');
    });
  });

  group('checkHealth not connected', () {
    test('ok false -> not connected', () async {
      final client = MockClient((req) async => obj({'ok': false}, 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('HTTP 500 with body {"ok":true} -> not connected', () async {
      final client = MockClient((req) async => obj({'ok': true}, 500));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('HTTP 404 -> not connected', () async {
      final client = MockClient((req) async => obj({'ok': true}, 404));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('HTTP 302 -> not connected', () async {
      final client = MockClient((req) async => raw('', 302));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('body "[]" -> not connected', () async {
      final client = MockClient((req) async => raw('[]', 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('body "\\"x\\"" -> not connected', () async {
      final client = MockClient((req) async => raw('"x"', 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('body "null" -> not connected', () async {
      final client = MockClient((req) async => raw('null', 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('empty body -> not connected', () async {
      final client = MockClient((req) async => raw('', 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('invalid UTF-8 bytes -> not connected, no exception', () async {
      final client =
          MockClient((req) async => http.Response.bytes([0xff, 0xfe, 0x00], 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('ok is 1 -> not connected', () async {
      final client = MockClient((req) async => obj({'ok': 1}, 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('ok is "true" -> not connected', () async {
      final client = MockClient((req) async => obj({'ok': 'true'}, 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('ok is null -> not connected', () async {
      final client = MockClient((req) async => obj({'ok': null}, 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('ok missing -> not connected', () async {
      final client = MockClient((req) async => obj(<String, Object?>{}, 200));
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('ClientException thrown by client -> not connected', () async {
      final client = MockClient((req) async {
        throw http.ClientException('boom');
      });
      expect(await checkHealth(client, base()), isA<HealthNotConnected>());
    });

    test('timeout -> not connected, no timer left', () async {
      final never = Completer<http.Response>();
      final client = MockClient((req) => never.future);
      final result = await checkHealth(client, base(),
          timeout: const Duration(milliseconds: 30));
      expect(result, isA<HealthNotConnected>());
    });
  });

  group('StringsVi', () {
    test('checkConnection label', () {
      expect(StringsVi.checkConnection, 'Kiểm tra kết nối');
    });

    test('notConnected label', () {
      expect(StringsVi.notConnected, 'Chưa kết nối được');
    });

    test('connected with version', () {
      expect(StringsVi.connected('final-2026-11-08'),
          'Đã kết nối (final-2026-11-08)');
      expect(StringsVi.connected('v2'), 'Đã kết nối (v2)');
    });

    test('connected without version', () {
      expect(StringsVi.connected(null), 'Đã kết nối');
    });
  });
}
