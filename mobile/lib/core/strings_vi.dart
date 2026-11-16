/// Câu chữ tiếng Việt của app (UC-12). Mọi chuỗi hiển thị chỉ đặt ở đây.
class StringsVi {
  const StringsVi._();

  static const String checkConnection = 'Kiểm tra kết nối';
  static const String notConnected = 'Chưa kết nối được';

  static String connected(String? modelVersion) =>
      modelVersion == null ? 'Đã kết nối' : 'Đã kết nối ($modelVersion)';
}
