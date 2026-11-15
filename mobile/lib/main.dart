import 'package:material_ui/material_ui.dart';

void main() {
  runApp(const MediCheckApp());
}

/// Khung app rỗng của ST-01; UI, theme và router thật sẽ có ở ST-02.
class MediCheckApp extends StatelessWidget {
  const MediCheckApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: SizedBox.shrink(),
    );
  }
}
