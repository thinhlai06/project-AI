import 'package:http/http.dart' as http;
import 'package:material_ui/material_ui.dart';

import 'features/settings/health_check_page.dart';

// TODO(ST-04.3): replace by the real SCR-SETTINGS with server address and connection test; remove the temporary address constant
const String _kDefaultServerAddress = 'http://10.0.2.2:8000';

void main() {
  runApp(const MediCheckApp());
}

/// Khung app của ST-01.3; UI, theme và router thật sẽ có ở ST-02/ST-04.
class MediCheckApp extends StatelessWidget {
  const MediCheckApp({super.key, this.client, this.baseUri});

  final http.Client? client;
  final Uri? baseUri;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HealthCheckPage(
        client: client ?? http.Client(),
        baseUri: baseUri ?? Uri.parse(_kDefaultServerAddress),
      ),
    );
  }
}
