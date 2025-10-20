# Public_012

# Các khái niệm cơ bản

## Khái niệm hệ điều hành

Hệ điều hành là một trong các phần mềm hệ thống có tính phổ dụng. Có nhiều cách diễn đạt khác nhau về hệ điều hành xuất phát từ góc độ của người sử dụng khác nhau. Tuy vậy có thể diễn đạt như sau:

_**Hệ điều hành là hệ thống chương trình đảm bảo quản lý tài nguyên của hệ thống tính toán và cung cấp các dịch vụ cho người sử dụng.**_

Thông thường trong các hệ máy tính hiện nay, hệ điều hành được cài đặt trên đĩa.

Nhiệm vụ cụ thể hơn của hệ điều hành là:

  * Khởi động máy tính, tạo môi trường giao tiếp cho người sử dụng.

  * Tự động điều khiển và kiểm soát hoạt động của các thiết bị (ổ đĩa, bàn phím, màn hình, máy in,…).

  * Quản lý việc cấp phát tài nguyên của máy tính như bộ xử lý trung ương, bộ nhớ, các thiết bị vào ra…

  * Quản lý các chương trình đang thực hiện trên máy tính.

  * Thực hiện giao tiếp với người sử dụng để nhận lệnh và thực hiện lệnh.


Hệ điều hành là phần mềm hệ thống, nên phụ thuộc vào cấu trúc của máy tính. Mỗi loại máy tính có hệ điều hành khác nhau. Ví dụ:

  * Máy tính lớn IBM360 có hệ điều hành là DOS, TOS.

  * Máy tính lớn EC-1022 có hệ điều hành là OC-EC.

  * Máy tính cá nhân PC-IBM có hệ điều hành MS-DOS.

  * Mạng máy tính có các hệ điều hành mạng NETWARE, UNIX, WINDOWS-NT…


## Tệp (File)

Tệp là tập hợp các dữ liệu có liên quan với nhau và được tổ chức theo 1 cấu trúc nào đó, thường được lưu trữ bên ngoài máy tính.

Nội dung của tệp có thể là chương trình, dữ liệu, văn bản,... Mỗi tập tin được lưu lên đĩa với một tên riêng phân biệt. Mỗi hệ điều hành có qui ước đặt tên khác nhau, tên tập tin thường có 2 phần: phần tên (name) và phần mở rộng (extension). Phần tên là phần bắt buộc phải có của một tập tin, còn phần mở rộng thì có thể có hoặc không.

  * Phần tên: Bao gồm các ký tự chữ từ A đến Z, các chữ số từ 0 đến 9, các ký tự khác như #, $, %, ~, ^, @, (, ), !, _, khoảng trắng. Phần tên do người tạo ra tập tin đặt. Với MS-DOS phần tên có tối đa là 8 ký tự, với Windows phần tên có thể đặt tối đa 128 ký tự.

  * Phần mở rộng: thường dùng 3 ký tự trong các ký tự nêu trên. Thông thường phần mở rộng do chương trình ứng dụng tạo ra tập tin tự đặt.

  * Giữa phần tên và phần mở rộng có một dấu chấm (.) ngăn cách.


Ta có thể căn cứ vào phần mở rộng để xác định kiểu của file:

  * COM, EXE : Các file khả thi chạy trực tiếp được trên hệ điều hành.

  * TXT, DOC, ... : Các file văn bản.

  * PAS, BAS, ... : Các file chương trình PASCAL, DELPHI, BASIC, ...

  * WK1, XLS, ... : Các file chương trình bảng tính LOTUS, EXCEL ...

  * BMP, GIF, JPG, ... : Các file hình ảnh.

  * MP3, DAT, WMA, … : Các file âm thanh, video.


_Ký hiệu đại diện (Wildcard)_

Để chỉ một nhóm các tập tin, ta có thể sử dụng hai ký hiệu đại diện:

  * Dấu ? dùng để đại diện cho một ký tự bất kỳ trong tên tập tin tại vị trí nó xuất hiện.

  * Dấu * dùng để đại diện cho một chuỗi ký tự bất kỳ trong tên tập tin từ vị trí nó xuất hiện.


Ví dụ:

Bai?.doc

Bai1.doc, Bai6.doc, Baiq.doc, …

Bai*.doc

Bai.doc, Bai6.doc, Bai12.doc, Bai Tap.doc, …

BaiTap.*

BaiTap.doc, BaiTap.xls, BaiTap.ppt, BaiTap.dbf, …

_Lưu ý_ : _Nên đặt tên mang tính gợi nhớ._

## Quản lý tệp của hệ điều hành

_Cấu trúc đĩa từ_

Hệ thống đĩa từ gồm nhiều mặt (side) gắn số hiệu là 0, 1,… Về mặt logic mỗi mặt đãi có một đầu ghi/ đọc (header), đôi khi người ta còn đồng nhất 2 khái niệm này. Mỗi mặt chia thành các rãnh (track - các đường tròn đồng tâm). Các rãnh được đánh số từ ngoài vào trong bắt đầu từ 0. Mỗi rãnh chia thành các cung (Sector), mỗi sector thông thường có dung lượng 512 byte. Một từ trụ (cylinder) gồm các rãnh có cùng bán kính nằm trên các mặt đĩa khác nhau.

_Tổ chức ghi thông tin trên đĩa_

Thông tin lưu trữ trên đĩa dưới dạng các tệp. Mỗi tệp chiếm 1 hoặc nhiều sectors tuỳ dung lượng tệp.

Để thuận lợi cho việc quản lý tệp, hệ điều hành cho phép chia đĩa thành các vùng, mỗi vùng chia thành các vùng con,.... Mỗi vùng có 1 vùng con riêng để lưu trữ thông tin về vùng đó, vùng con này được gọi là thư mục (Directory). Tệp được lưu trữ ở các vùng, vì vậy ta có thể thấy tổ chức lưu trữ này có dạng cây (Tree).

Thư mục là nơi lưu giữ các tập tin theo một chủ đề nào đó theo ý người sử dụng. Đây là biện pháp giúp ta quản lý được tập tin, dễ dàng tìm kiếm chúng khi cần truy xuất. Các tập tin có liên quan với nhau có thể được xếp trong cùng một thư mục. Sau đây là biểu tượng của thư mục hay còn gọi là Folder trong Windows

![](images/image2.jpeg)

Trên mỗi đĩa có một thư mục chung gọi là thư mục gốc. Thư mục gốc không có tên riêng và được ký hiệu là \ (dấu xổ phải: backslash). Dưới mỗi thư mục gốc có các tập tin trực thuộc và các thư mục con. Trong các thư mục con cũng có các tập tin trực thuộc và thư mục con của nó. Thư mục chứa thư mục con gọi là thư mục cha.

Thư mục đang làm việc gọi là thư mục hiện hành.
Tên của thư mục tuân thủ theo cách đặt tên của tập tin.

_Cách xác định tên đầy đủ của tệp_

Tên tệp đầy đủ gồm nơi lưu trữ tệp - đường dẫn từ gốc đến tệp (Path) và tên tệp. Đường dẫn được chỉ ra nhánh cây thư mục chứa tệp, trong đó sử dụng ký hiệu “\” ngăn cách tên các thư mục .

Ví dụ :

C:\TC\BIN\B1.C
…

Hệ điều hành được phân chia thành các phần, phù hợp với các chức năng riêng của công việc.

Những phần này được lưu trên đĩa dưới dạng các tệp (File). Ví dụ:

Hệ điều hành MS-DOS gồm tập các tệp, trong đó có 3 tệp cơ bản:

  * MSDOS.SYS - tệp.

  * IO.SYS - tệp điều khiển vào ra.

  * COMMAND.COM - tệp lệnh.


# Hệ lệnh của hệ điều hành

  * Thao tác với tệp: Sao chép, di chuyển, xoá, đổi tên , xem nội dung tệp

  * Thao tác với thư mục: tạo, xoá, sao chép

  * Thao tác với đĩa: tạo khuôn ( Format), sao chép đĩa


# Hệ điều hành Windows

## Sự ra đời và phát triển

Windows là một bộ chương trình do hãng Microsoft sản xuất. Từ version 3.0 ra đời vào tháng 5 năm 1990 đến nay, Microsoft đã không ngừng cải tiến làm cho môi trường này ngày càng được hoàn thiện.

**Windows 95** : vào cuối năm 1995, ở Việt nam đã xuất hiện một phiên bản mới của Windows mà chúng ta quen gọi là Windows 95. Những cải tiến mới của Windows 95 được liệt kê tóm tắt như sau:

  * Giao diện với người sử dụng được thiết kế lại hoàn toàn nên việc khởi động các chương trình ứng dụng cùng các công việc như mở và lưu cất các tư liệu, tổ chức các tài nguyên trên đĩa và nối kết với các hệ phục vụ trên mạng - tất cả đều trở nên đơn giản và dễ dàng hơn.

  * Cho phép đặt tên cho các tập tin dài đến 255 ký tự. Điều này rất quan trọng vì những tên dài sẽ giúp ta gợi nhớ đến nội dung của tập tin.

  * Hỗ trợ Plug and Play, cho phép tự động nhận diện các thiết bị ngoại vi nên việc cài đặt và quản lý chúng trở nên đơn giản hơn.

  * Hỗ trợ tốt hơn cho các ứng dụng Multimedia. Với sự tích hợp Audio và Video của Windows 95, máy tính cá nhân trở thành phương tiện giải trí không thể thiếu được.

  * Windows 95 là hệ điều hành 32 bit, vì vậy nó tăng cường sức mạnh và khả năng vận hành lên rất nhiều.

  * Trong Windows 95 có các công cụ đã được cải tiến nhằm chuẩn hoá, tối ưu hoá và điều chỉnh các sự cố. Điều này giúp bạn yên tâm hơn khi làm việc với máy vi tính trong môi trường của Windows 95.


Tóm lại, với những tính năng mới ưu việt và tích hợp cao, Windows 95 đã trở thành môi trường làm việc được người sử dụng ưa chuộng và tin dùng.

**Windows 98, Windows Me:** là những phiên bản tiếp theo của Windows 95, những phiên bản này tiếp tục phát huy và hoàn thiện những tính năng ưu việt của Windows 95 và tích hợp thêm những tính năng mới về Internet và Multimedia.

**Windows NT 4.0, Windows 2000, Windows XP, Windows 2003:** là những hệ điều hành được phát triển cao hơn, được dùng cho các cơ quan và doanh nghiệp. Giao diện của những hệ điều hành này tương tự như Windows 98/ Windows Me. Điểm khác biệt là những hệ điều hành này có tính năng bảo mật cao, vì vậy nó được sử dụng cho môi trường có nhiều người dùng.

**Windows VISTA,** đây là sản phẩm mới của MicroSoft hỗ trợ tốt cho các dịch vụ mạng, trò chơi, văn phòng,..

Giáo trình này sẽ trình bày dựa vào hệ điều hành Windows XP.

## Khởi động và thoát khỏi Windows XP

_Khởi động Windows XP_

Windows XP được tự động khởi động sau khi bật máy. Sẽ có thông báo yêu cầu nhập vào tài khoản (User name) và mật khẩu (Password) của người dùng. Thao tác này gọi là đăng nhập (logging on).

Mỗi người sử dụng sẽ có một tập hợp thông tin về các lựa chọn tự thiết lập cho mình (như bố trí màn hình, các chương trình tự động chạy khi khởi động máy, tài nguyên/ chương trình được phép sử dụng, v.v...) gọi là user profile và được Windows XP lưu giữ lại để sử dụng cho những lần khởi động sau.

_Thoát khỏi Windows XP:_

Khi muốn thoát khỏi Windows XP, bạn phải đóng tất cả các cửa sổ đang mở. Tiếp theo bạn nhấn tổ hợp phím Alt + F4 hoặc chọn menu Start (nếu không nhìn thấy nút Start ở phía dưới bên góc trái màn hình thì bạn nhấn tổ hợp phím Ctrl + Esc) và chọn Turn Off Computer. Sau thao tác này một hộp thoại sẽ xuất hiện như bên dưới.

Nếu bạn chọn Turn Off, ứng dụng đang làm việc sẽ được đóng lại và máy sẽ tự động tắt. Nếu vì một lý do nào đó mà máy tính không sẵn sàng để đóng (chưa lưu dữ liệu cho một ứng dụng hoặc sự trao đổi thông tin giữa hai máy nối mạng đang tiếp diễn v.v..) thì sẽ có thông báo để xử lý.

**Chú ý:** nếu không làm những thao tác đóng Windows như vừa nói ở trên mà tắt máy ngay thì có thể sẽ xảy ra việc thất lạc một phần của nội dung các tập tin dẫn đến trục trặc khi khởi động lại ở lần sử dụng tiếp theo.

## Một số thuật ngữ và thao tác thường sử dụng

_Biểu tượng_ ( _icon_ )

Biểu tượng là các hình vẽ nhỏ đặc trưng cho một đối tượng nào đó của Windows hoặc của các ứng dụng chạy trong môi trường Windows. Phía dưới biểu tượng là tên biểu tượng. Tên này mang một ý nghĩa nhất định, thông thường nó diễn giải cho chức năng được gán cho biểu tượng (ví dụ nó mang tên của 1 trình ứng dụng).

_Cửa sổ (Windows ):_

Cửa sổ là khung giao tiếp đồ họa của 1 ứng dụng hoặc 1 lệnh.

  * Bố cục của 1 cửa sổ : gồm thanh tiêu đề, thanh thực đơn, 1 số thành phần khác phụ thuộc vào loại cửa sổ,…

  * Các hộp giao tiếp

  * Các thao tác trên một cửa sổ

* Di chuyển cửa sổ: Drag thanh tiêu đề cửa sổ (Title bar) đến vị trí mới.

* Thay đổi kích thước của cửa sổ: Di chuyển con trỏ chuột đến cạnh hoặc góc cửa sổ, khi con trỏ chuột biến thành hình mũi tên hai chiều thì Drag cho đến khi đạt được kích thước mong muốn.

* Phóng to cửa sổ ra toàn màn hình: Click lên nút Maximize ![](images/image3.jpeg) .

* Phục hồi kích thước trước đó của cửa sổ: Click lên nút Restore ![](images/image4.jpeg) .

* Thu nhỏ cửa sổ thành biểu tượng trên Taskbar: Click lên nút Minimize ![](images/image5.jpeg) .

* Chuyển đổi giữa các cửa sổ của các ứng dụng đang mở: Để chuyển đổi giữa các ứng dụng nhấn tổ hợp phím Alt + Tab hoặc chọn ứng dụng tương ứng trên thanh

  * Taskbar.

* Đóng cửa sổ: Click lên nút Close ![](images/image6.jpeg) của cửa sổ hoặc nhấn tổ hợp phím Alt + F4.


_Hộp hội thoại (Dialogue box)_

Trong khi làm việc với Windows và các chương tình ứng dụng chạy dưới môi trường Windows bạn thường gặp những hộp hội thoại. Các hộp thoại này xuất hiện khi nó cần thêm những thông số để thực hiện lệnh theo yêu cầu của bạn. Hình dưới đây giới thiệu các thành phần của hộp hội thoại

Thông thường, trên một hộp hội thoại sẽ có các thành phần sau:

  * Hộp văn bản (Text box): dùng để nhập thông tin.

  * Hộp liệt kê (List box): liệt kê sẵn một danh sách có các mục có thể chọn lựa, nếu số mục trong danh sách nhiều không thể liệt kê hết thì sẽ xuất hiện thanh trượt để cuộn danh sách.

  * Hộp liệt kê thả (Drop down list box/ Combo box): khi nhắp chuột vào nút thả thì sẽ buông xuống một danh sách.

  * Hộp kiểm tra (Check box): có 2 dạng , dạng hình vuông thể hiện việc cho phép không

* chọn, chọn 1 hoặc nhiều mục không loại trừ lẫn nhau. Dạng ô tròn (Option button): bắt buộc phải chọn một trong số các mục. Đây là những lựa chọn loại trừ lẫn nhau.

  * Nút lệnh (Command Button): lệnh cần thực thi.Các loại nút lệnh thường gặp có:

* **OK( hoặc bấm phím Enter)** : thực hiện lệnh ( chấp nhận)

* **Close** : giữ lại các thông số đã chọn và đóng cửa sổ

* **Cancel** ( **hay nhấn phím Esc** ): không thực hiện lệnh ( từ chối thực hiện)

* **Apply** : áp dụng các thông số đã chọn.

* **Default** : đặt mặc định theo các thông số