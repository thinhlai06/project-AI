import 'package:flutter_test/flutter_test.dart';
import 'package:material_ui/material_ui.dart';

import 'package:mobile/main.dart';

void main() {
  testWidgets('app starts', (WidgetTester tester) async {
    await tester.pumpWidget(const MediCheckApp());
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
