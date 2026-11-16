import 'dart:async';
import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:material_ui/material_ui.dart';

import 'package:mobile/core/strings_vi.dart';
import 'package:mobile/features/settings/health_check_page.dart';
import 'package:mobile/main.dart';

/// MockClient trả về các future ta tự complete, để điều khiển thứ tự trả lời.
class _PendingClient {
  _PendingClient() {
    client = MockClient((req) {
      final completer = Completer<http.Response>();
      pending.add(completer);
      return completer.future;
    });
  }

  late final http.Client client;
  final List<Completer<http.Response>> pending = [];
}

void main() {
  Uri base() => Uri.parse('http://10.0.2.2:8000');

  http.Response ok([String? version]) => http.Response.bytes(
      utf8.encode(jsonEncode({'ok': true, 'model_version': version})), 200);

  http.Response fail() =>
      http.Response.bytes(utf8.encode('{"ok":false}'), 200);

  testWidgets('app starts', (tester) async {
    final client = MockClient((req) async => ok('final-2026-11-08'));
    await tester.pumpWidget(
        MediCheckApp(client: client, baseUri: base()));
    expect(find.byType(MaterialApp), findsOneWidget);
    await tester.pump();
  });

  testWidgets('shows connected text and one primary button on success',
      (tester) async {
    final p = _PendingClient();
    await tester.pumpWidget(MaterialApp(
        home: HealthCheckPage(client: p.client, baseUri: base())));
    await tester.pump();
    p.pending[0].complete(ok('final-2026-11-08'));
    await tester.pump();

    expect(find.text(StringsVi.connected('final-2026-11-08')), findsOneWidget);
    expect(find.byType(ElevatedButton), findsOneWidget);
    expect(
        find.byWidgetPredicate((w) =>
            w is Semantics &&
            w.properties.label == StringsVi.connected('final-2026-11-08')),
        findsOneWidget);
    expect(
        find.byWidgetPredicate((w) =>
            w is Semantics &&
            w.properties.button == true &&
            w.properties.label == StringsVi.checkConnection),
        findsOneWidget);

    final size = tester.getSize(find.byType(ElevatedButton));
    expect(size.height, greaterThanOrEqualTo(56));
    expect(size.width, greaterThanOrEqualTo(48));
    final label = tester.widget<Text>(find.text(StringsVi.checkConnection));
    expect(label.style?.fontSize, 20);
  });

  testWidgets('shows not connected text on failure', (tester) async {
    final p = _PendingClient();
    await tester.pumpWidget(MaterialApp(
        home: HealthCheckPage(client: p.client, baseUri: base())));
    await tester.pump();
    p.pending[0].complete(fail());
    await tester.pump();

    expect(find.text(StringsVi.notConnected), findsOneWidget);
    expect(find.text(StringsVi.connected(null)), findsNothing);
  });

  testWidgets('pressing again clears the old result before the new one',
      (tester) async {
    final p = _PendingClient();
    await tester.pumpWidget(MaterialApp(
        home: HealthCheckPage(client: p.client, baseUri: base())));
    await tester.pump();
    p.pending[0].complete(ok('v1'));
    await tester.pump();
    expect(find.text(StringsVi.connected('v1')), findsOneWidget);

    await tester.tap(find.byType(ElevatedButton));
    await tester.pump();

    // Old result gone while checking; button disabled; progress shown.
    expect(find.text(StringsVi.connected('v1')), findsNothing);
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    expect(
        tester.widget<ElevatedButton>(find.byType(ElevatedButton)).onPressed,
        isNull);
    expect(
        find.byWidgetPredicate((w) =>
            w is Semantics &&
            w.properties.label == StringsVi.checkConnection &&
            w.properties.button != true),
        findsOneWidget);

    p.pending[1].complete(fail());
    await tester.pump();
    expect(find.text(StringsVi.notConnected), findsOneWidget);
  });

  testWidgets('late reply of an older request does not overwrite a newer one',
      (tester) async {
    final p = _PendingClient();
    await tester.pumpWidget(MaterialApp(
        home: HealthCheckPage(client: p.client, baseUri: base())));
    await tester.pump();
    p.pending[0].complete(ok('v1'));
    await tester.pump();

    // The UI disables the button while checking, so force two overlapping
    // requests by invoking the captured callback directly.
    final onPressed =
        tester.widget<ElevatedButton>(find.byType(ElevatedButton)).onPressed!;
    onPressed();
    await tester.pump();
    onPressed();
    await tester.pump();
    expect(p.pending.length, 3);

    // Newer request (id 3) answers first.
    p.pending[2].complete(ok('v3'));
    await tester.pump();
    expect(find.text(StringsVi.connected('v3')), findsOneWidget);

    // Older request (id 2) answers late; must be ignored.
    p.pending[1].complete(fail());
    await tester.pump();
    expect(find.text(StringsVi.connected('v3')), findsOneWidget);
    expect(find.text(StringsVi.notConnected), findsNothing);
  });

  testWidgets('disposing while a request is pending does not throw',
      (tester) async {
    final p = _PendingClient();
    await tester.pumpWidget(MaterialApp(
        home: HealthCheckPage(client: p.client, baseUri: base())));
    await tester.pump();

    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pump();

    p.pending[0].complete(ok('v1'));
    await tester.pump();
  });
}
