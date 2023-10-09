# ContraGame

*******************************Các file được viết để tạo nên game Contra*******************************
1.	settings.py: Định nghĩa cấu hình chung cho toàn bộ game.
2.	entity.py: Định nghĩa lớp Entity chung cho các đối tượng trong game như player, enemy.
3.	tile.py: Định nghĩa lớp Tile làm map/môi trường cho game.
4.	player.py: Định nghĩa lớp Player kế thừa từ Entity cho nhân vật người chơi.
5.	enemy.py: Định nghĩa lớp Enemy kế thừa từ Entity cho các đối tượng enemy.
6.	bullet.py: Định nghĩa lớp Bullet cho đạn bắn.
7.	text.py: Định nghĩa lớp Text để hiển thị text trên màn hình.
8.	button.py: Định nghĩa lớp Button cho các nút trên giao diện.
9.	overlay.py: Định nghĩa lớp Overlay để vẽ các thông tin lên trên màn hình chính.
10.	all_sprites.py: Lớp chứa và vẽ tất cả các sprite lên màn hình.
11.	app.py: File khởi tạo ứng dụng, chứa game loop.
12.	start_menu.py: Định nghĩa scene menu bắt đầu game.
13.	game_over.py: Định nghĩa scene kết thúc game.
14.	main.py: Khởi động chương trình, gọi start_menu.
15.	setup.py: Đóng gói game thành file thực thi.


*******************************Chi tiết từng bước tạo game*******************************
1.	settings.py:
•	Định nghĩa các hằng số cài đặt cho game:
•	Kích thước màn hình
•	Các layer độ sâu cho các loại đối tượng
•	Đường dẫn tới các thư mục assets
2.	entity.py:
•	Định nghĩa lớp Entity chung cho các đối tượng như Player, Enemy.
•	Có các phương thức:
•	import_assets: load hình ảnh
•	shoot_timer: đếm thời gian để bắn
•	invul_timer: đếm thời gian không thể bị đánh trúng
•	damage: xử lý khi bị đánh trúng
•	check_death: kiểm tra có chết không
•	blink: nhấp nháy khi bị đánh trúng
animate: cập nhật animation

3.	tile.py 
•	Tile: Lớp cơ bản để vẽ các loại tile lên màn hình game. Có các thuộc tính:
•	image: Ảnh của tile
•	rect: vị trí của tile
•	z: layer để đặt tile lên trên hoặc dưới các đối tượng khác
•	CollisionTile: Kế thừa từ Tile, thêm chức năng va chạm. Có thêm thuộc tính:
•	old_rect: lưu vị trí tile ở frame trước, dùng để xử lý va chạm
•	MovingPlatform: Kế thừa từ CollisionTile, thêm chức năng di chuyển tile. Các thuộc tính mới:
•	direction: hướng di chuyển của platform
•	speed: tốc độ di chuyển
•	pos: vị trí dạng vector để tính toán di chuyển dựa trên phép tính số học
•	Phương thức update() của MovingPlatform dùng để cập nhật vị trí mới của platform dựa trên hướng và tốc độ di chuyển.

 
4.	player.py
•	Player
•	init: khởi tạo vị trí, hình ảnh, nhóm sprite
•	get_status: xác định trạng thái idle/jump/duck
•	check_contact: kiểm tra va chạm với các sprite để xác định có đứng trên sàn không
•	input: lấy input từ bàn phím và cập nhật trạng thái di chuyển, nhảy, bắn
•	collision: xử lý va chạm với các sprite khác
•	move: cập nhật vị trí dựa trên trạng thái và input
•	update:
•	Gọi các phương thức input, get_status, move
•	Gọi animate, check death

5.	enemy.py:
•	Enemy
•	init: khởi tạo vị trí, hình ảnh, nhóm sprite. Gán player để xác định hướng bắn.
•	get_status: xác định trạng thái quay phải/trái dựa vào vị trí so với player
•	check_fire: kiểm tra khoảng cách và bắn đạn nếu thỏa điều kiện
•	update:
•	Gọi get_status
•	Gọi animate
•	Gọi check_fire
•	Kiểm tra death

6.	bullet.py:
•	Bullet:
•	init: khởi tạo vị trí, hình ảnh, tốc độ, hướng di chuyển của đạn. Lưu thời gian bắt đầu.
•	update:
•	Cập nhật vị trí đạn dựa trên tốc độ và hướng di chuyển
•	Kiểm tra thời gian tồn tại, nếu vượt quá ngưỡng thì xóa đạn
•	kill: hủy đạn
•	FireAnimation:
•	init: khởi tạo animation bắn đạn ở vị trí súng
•	animate: cập nhật frame hiện tại của animation
•	move: cập nhật vị trí dựa trên vị trí súng
•	update: gọi animate và move

7.	text.py:
•	Định nghĩa lớp Text để vẽ chữ lên màn hình
•	Có các phương thức set_font, render, draw

8.	button.py:
•	Định nghĩa lớp Button dùng cho các nút trên menu.
•	Có các phương thức để vẽ nút, kiểm tra click chuột, thay đổi màu.
Như vậy mỗi file đảm nhiệm một chức năng riêng biệt trong game. Chúng kết hợp với nhau tạo thành một game hoàn chỉnh.

9.	overlay.py: vẽ các thông tin lên trên màn hình chính của game
•	Thuộc tính:
•	player: tham chiếu tới đối tượng Player để lấy thông tin hiển thị
•	display_surface: bề mặt để vẽ lên
•	health_surf: bề mặt chứa ảnh của 1 đơn vị thanh máu
•	display:
•	Duyệt vòng for bằng số máu hiện tại của người chơi
•	Tính toán tọa độ x, y để vẽ từng đơn vị ảnh thanh máu lên màn hình
•	Blit từng đơn vị ảnh lên màn hình theo tọa độ đã tính toán


10.	all_sprites.py:
•	Lớp AllSprites chứa và vẽ tất cả các sprite trong game.
•	Có hàm custom_draw để giữ nhân vật ở giữa màn hình.

11.	app.py:
•	Đây là file chính khởi tạo game, chứa lớp App.
•	Khởi tạo các biến Pygame cơ bản: màn hình, clock, âm thanh.
•	Khởi tạo các nhóm sprite: all_sprites, collision_sprites, platform_sprites, bullet_sprites.
•	Hàm load_map_layer: vẽ các tile trên map từ file tmx.
•	Hàm load_moving_platforms: tạo các platform di chuyển.
•	Hàm platform_collisions: xử lý va chạm giữa player và platform.
•	Hàm bullet_collisions: xử lý va chạm giữa đạn và các sprite.
•	Hàm shoot: bắn đạn.
•	Hàm load_player_and_enemies: tạo Player và Enemy từ tilemap.
•	Hàm setup: load tilemap, gọi các hàm tạo cảnh và nhân vật.
•	Hàm run: vòng lặp chính của game, handle events, cập nhật vị trí, hiển thị.

12.	start_menu.py:
•	Lớp StartMenu vẽ menu chính và xử lý các nút chơi, tùy chọn, thoát.
•	Gọi App().run() khi bấm nút Play.

13.	game_over.py:
•	Định nghĩa lớp GameOver hiển thị màn hình kết thúc game.
•	Có nút để chơi lại game.

14.	main.py:
•	File chính khởi động chương trình.
•	Import các thư viện cần thiết.
•	Khởi tạo đối tượng StartMenu và gọi hàm main_menu() để vào menu chính.

15.	setup.py:
•	Sử dụng thư viện cx_Freeze để đóng gói game thành file thực thi độc lập.
•	Định nghĩa các file và thư mục cần được đóng gói.
•	Tạo executable có tên targetName với entry point là main.py.
Như vậy:
•	main.py: File khởi động chương trình
•	settings.py: Cấu hình các thông số cho game
•	setup.py: Đóng gói thành file exe
Các file còn lại định nghĩa các scene, đối tượng, logic cho game.


