import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

/// Kết quả kiểm tra kết nối server (UC-12).
/// Tinh thần BR-01: lỗi không bao giờ được trông giống thành công.
sealed class HealthCheckResult {
  const HealthCheckResult();
}

/// Chỉ khi HTTP 200 + JSON object + ok đúng kiểu bool true.
final class HealthConnected extends HealthCheckResult {
  const HealthConnected(this.modelVersion);

  final String? modelVersion;
}

/// Mọi trường hợp còn lại.
final class HealthNotConnected extends HealthCheckResult {
  const HealthNotConnected();
}

/// Gọi `GET {baseUri}/health`, trả kết quả có kiểu, không ném lỗi,
/// không log nội dung trả lời (BR-10).
Future<HealthCheckResult> checkHealth(
  http.Client client,
  Uri baseUri, {
  Duration timeout = const Duration(seconds: 10),
}) async {
  try {
    final response =
        await client.get(baseUri.resolve('/health')).timeout(timeout);
    if (response.statusCode != 200) {
      return const HealthNotConnected();
    }
    final Object? decoded = jsonDecode(utf8.decode(response.bodyBytes));
    if (decoded is! Map<String, dynamic>) {
      return const HealthNotConnected();
    }
    final Object? ok = decoded['ok'];
    if (ok is bool && ok == true) {
      final Object? version = decoded['model_version'];
      return HealthConnected(version is String ? version : null);
    }
    return const HealthNotConnected();
  } on TimeoutException {
    return const HealthNotConnected();
  } on FormatException {
    return const HealthNotConnected();
  } catch (_) {
    return const HealthNotConnected();
  }
}
