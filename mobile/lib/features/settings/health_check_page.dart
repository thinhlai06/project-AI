import 'package:http/http.dart' as http;
import 'package:material_ui/material_ui.dart';

import '../../core/api/health_check.dart';
import '../../core/strings_vi.dart';

// TODO(ST-04.3): replace by the real SCR-SETTINGS with server address and connection test; remove the temporary address constant
// TODO(ST-02.1): use design tokens for sizes
class HealthCheckPage extends StatefulWidget {
  const HealthCheckPage({
    super.key,
    required this.client,
    required this.baseUri,
  });

  final http.Client client;
  final Uri baseUri;

  @override
  State<HealthCheckPage> createState() => _HealthCheckPageState();
}

class _HealthCheckPageState extends State<HealthCheckPage> {
  int _requestId = 0;
  bool _checking = false;
  HealthCheckResult? _result;

  @override
  void initState() {
    super.initState();
    _checking = true;
    _result = null;
    _awaitCheck(++_requestId);
  }

  void _onPressed() {
    final id = ++_requestId;
    setState(() {
      _checking = true;
      _result = null;
    });
    _awaitCheck(id);
  }

  Future<void> _awaitCheck(int id) async {
    final result = await checkHealth(widget.client, widget.baseUri);
    // Bỏ qua trả lời cũ/muộn và không setState sau khi dispose.
    if (!mounted || id != _requestId) {
      return;
    }
    setState(() {
      _checking = false;
      _result = result;
    });
  }

  @override
  Widget build(BuildContext context) {
    final result = _result;
    String? resultText;
    if (result is HealthConnected) {
      resultText = StringsVi.connected(result.modelVersion);
    } else if (result is HealthNotConnected) {
      resultText = StringsVi.notConnected;
    }

    return Scaffold(
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Semantics(
              label: StringsVi.checkConnection,
              button: true,
              child: SizedBox(
                height: 56,
                child: ElevatedButton(
                  onPressed: _checking ? null : _onPressed,
                  child: _checking
                      ? Semantics(
                          label: StringsVi.checkConnection,
                          child: const CircularProgressIndicator(),
                        )
                      : const Text(
                          StringsVi.checkConnection,
                          style: TextStyle(fontSize: 20),
                        ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            if (resultText != null)
              Semantics(
                label: resultText,
                child: Text(
                  resultText,
                  style: const TextStyle(fontSize: 20),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
