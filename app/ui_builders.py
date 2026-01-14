from PyQt6 import QtCore, QtGui, QtWidgets
from qfluentwidgets import (
    LineEdit,
    ListWidget,
    PrimaryPushButton,
    PushButton,
    ScrollArea,
    ComboBox,
    SwitchButton,
    SubtitleLabel,
    TitleLabel,
    StrongBodyLabel,
    TransparentToolButton,
    HorizontalSeparator,
    IndeterminateProgressBar,
)
from app.home_cards import CardFlowContainer, DraggableCard
from qfluentwidgets.components.widgets.card_widget import SimpleCardWidget
from qfluentwidgets import FluentIcon as FIF


def build_home_page(window) -> None:
    window.home_page = QtWidgets.QWidget()
    window.home_page.setObjectName('homePage')
    home_layout = QtWidgets.QVBoxLayout(window.home_page)
    home_layout.setContentsMargins(24, 24, 24, 24)
    home_layout.setSpacing(12)
    home_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    home_header = QtWidgets.QHBoxLayout()
    home_header.setSpacing(12)
    title_stack = QtWidgets.QVBoxLayout()
    title_stack.setSpacing(4)
    window.home_title = TitleLabel('')
    title_stack.addWidget(window.home_title)
    window.home_subtitle = SubtitleLabel('')
    window.home_subtitle.setWordWrap(True)
    window.home_subtitle.setVisible(False)
    title_stack.addWidget(window.home_subtitle)
    home_header.addLayout(title_stack, 1)

    action_stack = QtWidgets.QHBoxLayout()
    action_stack.setSpacing(6)
    window.home_add_card_btn = TransparentToolButton(FIF.ADD)
    window.home_add_card_btn.clicked.connect(window._show_add_card_menu)
    window.home_add_card_btn.setVisible(False)
    window.home_edit_btn = TransparentToolButton(FIF.EDIT)
    window.home_edit_btn.clicked.connect(window._toggle_home_edit_mode)
    action_stack.addWidget(window.home_add_card_btn)
    action_stack.addWidget(window.home_edit_btn)
    home_header.addLayout(action_stack)
    home_layout.addLayout(home_header)

    home_layout.addWidget(HorizontalSeparator())
    window.home_quick_label = StrongBodyLabel('')
    home_layout.addWidget(window.home_quick_label)

    home_scroll = ScrollArea()
    home_scroll.setWidgetResizable(True)
    home_scroll.setStyleSheet(
        'QScrollArea { border: none; background: transparent; }'
        'QScrollArea > QWidget > QWidget { background: transparent; }'
    )
    home_layout.addWidget(home_scroll, 1)

    window.home_card_container = CardFlowContainer()
    window.home_card_container.setStyleSheet('background: transparent;')
    home_scroll.setWidget(window.home_card_container)

    window.home_greeting_card = DraggableCard('greeting')
    window.home_greeting_card.setFixedWidth(360)
    greeting_layout = QtWidgets.QVBoxLayout(window.home_greeting_card)
    greeting_layout.setContentsMargins(16, 14, 16, 14)
    greeting_layout.setSpacing(8)

    greeting_header = QtWidgets.QHBoxLayout()
    greeting_header.addStretch(1)
    window.home_greeting_delete = TransparentToolButton(FIF.CLOSE)
    window.home_greeting_delete.clicked.connect(lambda: window._hide_home_card('greeting'))
    greeting_header.addWidget(window.home_greeting_delete)
    greeting_layout.addLayout(greeting_header)
    window.home_greeting_card.set_delete_button(window.home_greeting_delete)

    window.home_greeting_body = SubtitleLabel('')
    window.home_greeting_body.setTextFormat(QtCore.Qt.TextFormat.RichText)
    window.home_greeting_body.setWordWrap(True)
    greeting_layout.addWidget(window.home_greeting_body)
    greeting_layout.addStretch(1)
    window.home_card_container.add_card(window.home_greeting_card)

    window.home_profile_card = DraggableCard('profile')
    window.home_profile_card.setFixedWidth(360)
    profile_layout = QtWidgets.QVBoxLayout(window.home_profile_card)
    profile_layout.setContentsMargins(16, 14, 16, 14)
    profile_layout.setSpacing(8)

    profile_header = QtWidgets.QHBoxLayout()
    window.home_profile_label = SubtitleLabel('')
    profile_header.addWidget(window.home_profile_label)
    profile_header.addStretch(1)
    window.home_profile_delete = TransparentToolButton(FIF.CLOSE)
    window.home_profile_delete.clicked.connect(lambda: window._hide_home_card('profile'))
    profile_header.addWidget(window.home_profile_delete)
    profile_layout.addLayout(profile_header)
    window.home_profile_card.set_delete_button(window.home_profile_delete)

    window.home_profile_hint = SubtitleLabel('')
    window.home_profile_hint.setWordWrap(True)
    profile_layout.addWidget(window.home_profile_hint)

    home_buttons = QtWidgets.QHBoxLayout()
    window.home_launch_btn = PrimaryPushButton('')
    window.home_launch_btn.setIcon(FIF.PLAY)
    window.home_launch_btn.clicked.connect(lambda: window.switchTo(window.launch_page))
    window.home_profiles_btn = PushButton('')
    window.home_profiles_btn.setIcon(FIF.PEOPLE)
    window.home_profiles_btn.clicked.connect(lambda: window.switchTo(window.profiles_page))
    home_buttons.addWidget(window.home_launch_btn)
    home_buttons.addWidget(window.home_profiles_btn)
    home_buttons.addStretch(1)
    profile_layout.addLayout(home_buttons)
    window.home_card_container.add_card(window.home_profile_card)

    window.home_tips_card = DraggableCard('tips')
    window.home_tips_card.setFixedWidth(360)
    tips_layout = QtWidgets.QVBoxLayout(window.home_tips_card)
    tips_layout.setContentsMargins(16, 14, 16, 14)
    tips_layout.setSpacing(8)

    tips_header = QtWidgets.QHBoxLayout()
    window.home_tips_label = SubtitleLabel('')
    tips_header.addWidget(window.home_tips_label)
    tips_header.addStretch(1)
    window.home_tips_delete = TransparentToolButton(FIF.CLOSE)
    window.home_tips_delete.clicked.connect(lambda: window._hide_home_card('tips'))
    tips_header.addWidget(window.home_tips_delete)
    tips_layout.addLayout(tips_header)
    window.home_tips_card.set_delete_button(window.home_tips_delete)

    window.home_tips_body = SubtitleLabel('')
    window.home_tips_body.setWordWrap(True)
    tips_layout.addWidget(window.home_tips_body)
    tips_layout.addStretch(1)
    window.home_card_container.add_card(window.home_tips_card)


def build_launch_page(window) -> None:
    window.launch_page = QtWidgets.QWidget()
    window.launch_page.setObjectName('launchPage')
    launch_layout = QtWidgets.QVBoxLayout(window.launch_page)
    launch_layout.setContentsMargins(24, 24, 24, 24)
    launch_layout.setSpacing(16)
    launch_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    window.launch_title = TitleLabel('')
    launch_layout.addWidget(window.launch_title)

    window.launch_subtitle = SubtitleLabel('')
    launch_layout.addWidget(window.launch_subtitle)

    window.launch_card = SimpleCardWidget()
    launch_card_layout = QtWidgets.QVBoxLayout(window.launch_card)
    launch_card_layout.setContentsMargins(16, 12, 16, 16)
    launch_card_layout.setSpacing(10)

    window.launch_group_title = StrongBodyLabel('')
    launch_card_layout.addWidget(window.launch_group_title)
    launch_card_layout.addWidget(HorizontalSeparator())

    launch_form_container = QtWidgets.QWidget()
    launch_form = QtWidgets.QFormLayout(launch_form_container)
    launch_form.setVerticalSpacing(10)
    launch_form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

    window.launch_profile_combo = ComboBox()
    window.launch_profile_combo.currentIndexChanged.connect(window._on_launch_profile_changed)
    window.launch_label_profile = QtWidgets.QLabel()
    launch_form.addRow(window.launch_label_profile, window.launch_profile_combo)

    window.url_input = LineEdit()
    window.url_input.setPlaceholderText('https://example.com')
    window.launch_label_url = QtWidgets.QLabel()
    launch_form.addRow(window.launch_label_url, window.url_input)

    launch_card_layout.addWidget(launch_form_container)
    launch_layout.addWidget(window.launch_card)

    launch_actions = QtWidgets.QHBoxLayout()
    window.open_btn = PrimaryPushButton('')
    window.open_btn.setIcon(FIF.PLAY)
    window.open_btn.clicked.connect(window._open_browser)
    window.launch_profiles_btn = PushButton('')
    window.launch_profiles_btn.setIcon(FIF.PEOPLE)
    window.launch_profiles_btn.clicked.connect(lambda: window.switchTo(window.profiles_page))
    launch_actions.addWidget(window.open_btn)
    launch_actions.addWidget(window.launch_profiles_btn)
    launch_actions.addStretch(1)
    launch_layout.addLayout(launch_actions)
    launch_layout.addStretch(1)


def build_profiles_page(window) -> None:
    window.profiles_page = QtWidgets.QWidget()
    window.profiles_page.setObjectName('profilesPage')
    profiles_outer = QtWidgets.QVBoxLayout(window.profiles_page)
    profiles_outer.setContentsMargins(0, 0, 0, 0)
    profiles_outer.setSpacing(0)

    profiles_scroll = ScrollArea()
    profiles_scroll.setWidgetResizable(True)
    profiles_scroll.setStyleSheet(
        'QScrollArea { border: none; background: transparent; }'
        'QScrollArea > QWidget > QWidget { background: transparent; }'
    )
    profiles_outer.addWidget(profiles_scroll)

    window.profiles_content = QtWidgets.QWidget()
    window.profiles_content.setStyleSheet('background: transparent;')
    profiles_scroll.setWidget(window.profiles_content)

    root_layout = QtWidgets.QHBoxLayout(window.profiles_content)
    root_layout.setContentsMargins(16, 16, 16, 16)
    root_layout.setSpacing(16)
    root_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    left_panel = QtWidgets.QWidget()
    left_panel.setStyleSheet('background: transparent;')
    left_layout = QtWidgets.QVBoxLayout(left_panel)
    left_layout.setContentsMargins(12, 12, 12, 12)
    left_layout.setSpacing(12)
    left_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    window.profiles_title = TitleLabel('')
    left_layout.addWidget(window.profiles_title)

    window.profile_list = ListWidget()
    window.profile_list.currentItemChanged.connect(window._on_profile_selected)

    list_scroll = ScrollArea()
    list_scroll.setWidgetResizable(True)
    list_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    list_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    list_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    list_scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')
    list_container = QtWidgets.QWidget()
    list_container.setStyleSheet('background: transparent;')
    list_scroll.setWidget(list_container)
    list_layout = QtWidgets.QVBoxLayout(list_container)
    list_layout.setContentsMargins(0, 0, 0, 0)
    list_layout.addWidget(window.profile_list)
    left_layout.addWidget(list_scroll, 1)

    window.actions_label = SubtitleLabel('')
    left_layout.addWidget(window.actions_label)

    window.new_random_btn = PushButton('')
    window.new_random_btn.setIcon(FIF.ADD)
    window.new_random_btn.clicked.connect(window._create_random_profile)
    left_layout.addWidget(window.new_random_btn)

    window.new_ip_btn = PushButton('')
    window.new_ip_btn.setIcon(FIF.GLOBE)
    window.new_ip_btn.clicked.connect(window._create_ip_profile)
    left_layout.addWidget(window.new_ip_btn)

    window.delete_btn = PushButton('')
    window.delete_btn.setIcon(FIF.DELETE)
    window.delete_btn.clicked.connect(window._delete_profile)
    left_layout.addWidget(window.delete_btn)

    window.refresh_btn = PushButton('')
    window.refresh_btn.setIcon(FIF.SYNC)
    window.refresh_btn.clicked.connect(window.refresh_profiles)
    left_layout.addWidget(window.refresh_btn)

    root_layout.addWidget(left_panel, 1)

    right_panel = QtWidgets.QWidget()
    right_panel.setStyleSheet('background: transparent;')
    right_layout = QtWidgets.QVBoxLayout(right_panel)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(0)
    right_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    config_scroll = ScrollArea()
    config_scroll.setWidgetResizable(True)
    config_scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    config_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    config_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    config_scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')
    right_layout.addWidget(config_scroll)

    config_container = QtWidgets.QWidget()
    config_container.setStyleSheet('background: transparent;')
    config_scroll.setWidget(config_container)
    config_layout = QtWidgets.QVBoxLayout(config_container)
    config_layout.setContentsMargins(12, 12, 12, 12)
    config_layout.setSpacing(12)
    config_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    window.details_header = TitleLabel('')
    config_layout.addWidget(window.details_header)

    window.details_card = SimpleCardWidget()
    window.details_card.setObjectName('detailsCard')
    details_layout = QtWidgets.QVBoxLayout(window.details_card)
    details_layout.setContentsMargins(16, 12, 16, 16)
    details_layout.setSpacing(10)
    details_form_container = QtWidgets.QWidget()
    form = QtWidgets.QFormLayout(details_form_container)
    form.setVerticalSpacing(10)
    form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

    window.field_profile_id = LineEdit()
    window.field_profile_id.setReadOnly(True)
    window.label_profile_id = QtWidgets.QLabel()
    form.addRow(window.label_profile_id, window.field_profile_id)

    window.field_user_agent = LineEdit()
    window.field_user_agent.setReadOnly(False)
    window.field_user_agent.editingFinished.connect(
        lambda: window._on_profile_text_changed('user_agent', window.field_user_agent)
    )
    window.label_user_agent = QtWidgets.QLabel()
    form.addRow(window.label_user_agent, window.field_user_agent)

    window.profile_browser_combo = ComboBox()
    window.profile_browser_combo.currentIndexChanged.connect(window._on_profile_browser_changed)
    window.label_profile_browser = QtWidgets.QLabel()
    form.addRow(window.label_profile_browser, window.profile_browser_combo)

    window.field_timezone = LineEdit()
    window.field_timezone.setReadOnly(False)
    window.field_timezone.editingFinished.connect(
        lambda: window._on_profile_text_changed('timezone', window.field_timezone)
    )
    window.label_timezone = QtWidgets.QLabel()
    form.addRow(window.label_timezone, window.field_timezone)

    window.field_locale = LineEdit()
    window.field_locale.setReadOnly(False)
    window.field_locale.editingFinished.connect(
        lambda: window._on_profile_text_changed('locale', window.field_locale)
    )
    window.label_locale = QtWidgets.QLabel()
    form.addRow(window.label_locale, window.field_locale)

    window.field_screen = LineEdit()
    window.field_screen.setReadOnly(False)
    window.field_screen.editingFinished.connect(window._on_profile_screen_changed)
    window.label_screen = QtWidgets.QLabel()
    form.addRow(window.label_screen, window.field_screen)

    window.field_pixel_ratio = LineEdit()
    window.field_pixel_ratio.setReadOnly(False)
    window.field_pixel_ratio.editingFinished.connect(window._on_profile_pixel_ratio_changed)
    window.label_pixel_ratio = QtWidgets.QLabel()
    form.addRow(window.label_pixel_ratio, window.field_pixel_ratio)

    window.field_hardware = LineEdit()
    window.field_hardware.setReadOnly(False)
    window.field_hardware.editingFinished.connect(window._on_profile_hardware_changed)
    window.label_hardware = QtWidgets.QLabel()
    form.addRow(window.label_hardware, window.field_hardware)

    window.field_webgl = LineEdit()
    window.field_webgl.setReadOnly(False)
    window.field_webgl.editingFinished.connect(
        lambda: window._on_profile_text_changed('webgl_renderer', window.field_webgl)
    )
    window.label_webgl = QtWidgets.QLabel()
    form.addRow(window.label_webgl, window.field_webgl)

    window.field_geo = LineEdit()
    window.field_geo.setReadOnly(False)
    window.field_geo.editingFinished.connect(window._on_profile_geo_changed)
    window.label_geo = QtWidgets.QLabel()
    form.addRow(window.label_geo, window.field_geo)

    details_layout.addWidget(details_form_container)
    config_layout.addWidget(window.details_card)

    window.protection_header = StrongBodyLabel('')
    config_layout.addWidget(window.protection_header)
    window.protection_card = SimpleCardWidget()
    protection_layout = QtWidgets.QVBoxLayout(window.protection_card)
    protection_layout.setContentsMargins(16, 12, 16, 16)
    protection_layout.setSpacing(10)
    protection_form_container = QtWidgets.QWidget()
    protection_form = QtWidgets.QFormLayout(protection_form_container)
    protection_form.setVerticalSpacing(12)
    protection_form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

    window.switch_webrtc = SwitchButton('Off')
    window.switch_webrtc.setOnText('On')
    window.switch_webrtc.checkedChanged.connect(window._on_protection_changed)
    window.label_webrtc = QtWidgets.QLabel()
    protection_form.addRow(window.label_webrtc, window.switch_webrtc)

    window.switch_canvas = SwitchButton('Off')
    window.switch_canvas.setOnText('On')
    window.switch_canvas.checkedChanged.connect(window._on_protection_changed)
    window.label_canvas = QtWidgets.QLabel()
    protection_form.addRow(window.label_canvas, window.switch_canvas)

    window.switch_webgl = SwitchButton('Off')
    window.switch_webgl.setOnText('On')
    window.switch_webgl.checkedChanged.connect(window._on_protection_changed)
    window.label_webgl_protect = QtWidgets.QLabel()
    protection_form.addRow(window.label_webgl_protect, window.switch_webgl)

    window.switch_audio = SwitchButton('Off')
    window.switch_audio.setOnText('On')
    window.switch_audio.checkedChanged.connect(window._on_protection_changed)
    window.label_audio = QtWidgets.QLabel()
    protection_form.addRow(window.label_audio, window.switch_audio)

    window.switch_fonts = SwitchButton('Off')
    window.switch_fonts.setOnText('On')
    window.switch_fonts.checkedChanged.connect(window._on_protection_changed)
    window.label_fonts = QtWidgets.QLabel()
    protection_form.addRow(window.label_fonts, window.switch_fonts)

    window.switch_geolocation = SwitchButton('Off')
    window.switch_geolocation.setOnText('On')
    window.switch_geolocation.checkedChanged.connect(window._on_protection_changed)
    window.label_geolocation = QtWidgets.QLabel()
    protection_form.addRow(window.label_geolocation, window.switch_geolocation)

    window.switch_timezone = SwitchButton('Off')
    window.switch_timezone.setOnText('On')
    window.switch_timezone.checkedChanged.connect(window._on_protection_changed)
    window.label_timezone_protect = QtWidgets.QLabel()
    protection_form.addRow(window.label_timezone_protect, window.switch_timezone)

    window.switch_client_hints = SwitchButton('Off')
    window.switch_client_hints.setOnText('On')
    window.switch_client_hints.checkedChanged.connect(window._on_protection_changed)
    window.label_client_hints = QtWidgets.QLabel()
    protection_form.addRow(window.label_client_hints, window.switch_client_hints)

    window._protection_switches = [
        window.switch_webrtc,
        window.switch_canvas,
        window.switch_webgl,
        window.switch_audio,
        window.switch_fonts,
        window.switch_geolocation,
        window.switch_timezone,
        window.switch_client_hints,
    ]

    protection_layout.addWidget(protection_form_container)
    config_layout.addWidget(window.protection_card)

    window.fingerprint_header = StrongBodyLabel('')
    config_layout.addWidget(window.fingerprint_header)
    window.fingerprint_card = SimpleCardWidget()
    fingerprint_layout = QtWidgets.QVBoxLayout(window.fingerprint_card)
    fingerprint_layout.setContentsMargins(16, 12, 16, 16)
    fingerprint_layout.setSpacing(10)
    fingerprint_form_container = QtWidgets.QWidget()
    fingerprint_form = QtWidgets.QFormLayout(fingerprint_form_container)
    fingerprint_form.setVerticalSpacing(10)
    fingerprint_form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

    window.combo_webrtc_mode = ComboBox()
    window.combo_webrtc_mode.currentIndexChanged.connect(
        lambda idx: window._on_profile_combo_changed('webrtc_mode', window.combo_webrtc_mode)
    )
    window.label_webrtc_mode = QtWidgets.QLabel()
    fingerprint_form.addRow(window.label_webrtc_mode, window.combo_webrtc_mode)

    fingerprint_layout.addWidget(fingerprint_form_container)
    config_layout.addWidget(window.fingerprint_card)
    config_layout.addStretch(1)
    root_layout.addWidget(right_panel, 2)


def build_settings_page(window) -> None:
    window.settings_page = QtWidgets.QWidget()
    window.settings_page.setObjectName('settingsPage')
    settings_layout = QtWidgets.QVBoxLayout(window.settings_page)
    settings_layout.setContentsMargins(24, 24, 24, 24)
    settings_layout.setSpacing(16)
    settings_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    window.settings_title = TitleLabel('')
    settings_layout.addWidget(window.settings_title)

    window.settings_subtitle = SubtitleLabel('')
    settings_layout.addWidget(window.settings_subtitle)

    window.settings_card = SimpleCardWidget()
    settings_card_layout = QtWidgets.QVBoxLayout(window.settings_card)
    settings_card_layout.setContentsMargins(16, 12, 16, 16)
    settings_card_layout.setSpacing(10)
    window.settings_group_title = StrongBodyLabel('')
    settings_card_layout.addWidget(window.settings_group_title)
    settings_card_layout.addWidget(HorizontalSeparator())
    settings_form_container = QtWidgets.QWidget()
    settings_form = QtWidgets.QFormLayout(settings_form_container)
    settings_form.setVerticalSpacing(10)
    settings_form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

    window.settings_label_language = QtWidgets.QLabel()
    window.language_combo = ComboBox()
    window.language_combo.currentIndexChanged.connect(window._on_language_changed)
    settings_form.addRow(window.settings_label_language, window.language_combo)

    window.settings_label_theme = QtWidgets.QLabel()
    window.theme_combo = ComboBox()
    window.theme_combo.currentIndexChanged.connect(window._on_theme_changed)
    settings_form.addRow(window.settings_label_theme, window.theme_combo)

    settings_card_layout.addWidget(settings_form_container)
    window.settings_onboarding_btn = PushButton('')
    window.settings_onboarding_btn.setIcon(FIF.PLAY)
    window.settings_onboarding_btn.clicked.connect(window._show_onboarding)
    settings_card_layout.addWidget(window.settings_onboarding_btn)
    settings_layout.addWidget(window.settings_card)
    settings_layout.addStretch(1)


def build_onboarding_page(window) -> None:
    window.onboarding_page = QtWidgets.QWidget()
    window.onboarding_page.setObjectName('onboardingPage')
    layout = QtWidgets.QVBoxLayout(window.onboarding_page)
    layout.setContentsMargins(32, 32, 32, 32)
    layout.setSpacing(16)
    layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    window.onboarding_stack = QtWidgets.QStackedWidget()
    layout.addWidget(window.onboarding_stack, 1)

    welcome_page = QtWidgets.QWidget()
    welcome_layout = QtWidgets.QVBoxLayout(welcome_page)
    welcome_layout.setContentsMargins(0, 0, 0, 0)
    welcome_layout.setSpacing(12)
    window.onboarding_welcome_title = TitleLabel('')
    window.onboarding_welcome_body = SubtitleLabel('')
    window.onboarding_welcome_body.setWordWrap(True)
    welcome_layout.addWidget(window.onboarding_welcome_title)
    welcome_layout.addWidget(window.onboarding_welcome_body)
    welcome_layout.addStretch(1)

    install_page = QtWidgets.QWidget()
    install_layout = QtWidgets.QVBoxLayout(install_page)
    install_layout.setContentsMargins(0, 0, 0, 0)
    install_layout.setSpacing(12)
    window.onboarding_install_title = TitleLabel('')
    install_layout.addWidget(window.onboarding_install_title)
    window.onboarding_install_desc = SubtitleLabel('')
    window.onboarding_install_desc.setWordWrap(True)
    install_layout.addWidget(window.onboarding_install_desc)
    install_card = SimpleCardWidget()
    install_card_layout = QtWidgets.QVBoxLayout(install_card)
    install_card_layout.setContentsMargins(16, 12, 16, 16)
    install_card_layout.setSpacing(10)
    form_container = QtWidgets.QWidget()
    form = QtWidgets.QFormLayout(form_container)
    form.setVerticalSpacing(10)
    form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    window.onboarding_install_version_combo = ComboBox()
    window.onboarding_install_version_combo.currentIndexChanged.connect(
        window._on_install_version_changed
    )
    window.onboarding_install_version_label = QtWidgets.QLabel()
    form.addRow(window.onboarding_install_version_label, window.onboarding_install_version_combo)
    install_card_layout.addWidget(form_container)
    action_row = QtWidgets.QHBoxLayout()
    window.onboarding_install_btn = PrimaryPushButton('')
    window.onboarding_install_btn.setIcon(FIF.SYNC)
    window.onboarding_install_btn.clicked.connect(window._start_install_browser)
    action_row.addWidget(window.onboarding_install_btn)
    action_row.addStretch(1)
    install_card_layout.addLayout(action_row)
    window.onboarding_install_progress = IndeterminateProgressBar()
    window.onboarding_install_progress.setVisible(False)
    install_card_layout.addWidget(window.onboarding_install_progress)
    install_layout.addWidget(install_card)
    install_layout.addStretch(1)

    init_page = QtWidgets.QWidget()
    init_layout = QtWidgets.QVBoxLayout(init_page)
    init_layout.setContentsMargins(0, 0, 0, 0)
    init_layout.setSpacing(12)
    window.onboarding_init_title = TitleLabel('')
    window.onboarding_init_desc = SubtitleLabel('')
    window.onboarding_init_desc.setWordWrap(True)
    init_layout.addWidget(window.onboarding_init_title)
    init_layout.addWidget(window.onboarding_init_desc)
    init_actions = QtWidgets.QHBoxLayout()
    window.onboarding_init_btn = PrimaryPushButton('')
    window.onboarding_init_btn.setIcon(FIF.ADD)
    window.onboarding_init_btn.clicked.connect(window._onboarding_init_profile)
    init_actions.addWidget(window.onboarding_init_btn)
    init_actions.addStretch(1)
    init_layout.addLayout(init_actions)
    init_layout.addStretch(1)

    window.onboarding_stack.addWidget(welcome_page)
    window.onboarding_stack.addWidget(install_page)
    window.onboarding_stack.addWidget(init_page)

    footer = QtWidgets.QHBoxLayout()
    window.onboarding_back_btn = PushButton('')
    window.onboarding_back_btn.clicked.connect(window._onboarding_prev_step)
    window.onboarding_next_btn = PrimaryPushButton('')
    window.onboarding_next_btn.clicked.connect(window._onboarding_next_step)
    window.onboarding_exit_btn = PushButton('')
    window.onboarding_exit_btn.clicked.connect(window._onboarding_exit)
    footer.addWidget(window.onboarding_back_btn)
    footer.addWidget(window.onboarding_next_btn)
    footer.addStretch(1)
    footer.addWidget(window.onboarding_exit_btn)
    layout.addLayout(footer)


def build_browser_library_page(window) -> None:
    window.browser_library_page = QtWidgets.QWidget()
    window.browser_library_page.setObjectName('browserLibraryPage')
    layout = QtWidgets.QVBoxLayout(window.browser_library_page)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)
    layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    header_row = QtWidgets.QHBoxLayout()
    header_row.setSpacing(12)
    title_stack = QtWidgets.QVBoxLayout()
    title_stack.setSpacing(4)
    window.browser_library_title = TitleLabel('')
    title_stack.addWidget(window.browser_library_title)
    window.browser_library_subtitle = SubtitleLabel('')
    title_stack.addWidget(window.browser_library_subtitle)
    header_row.addLayout(title_stack, 1)
    window.browser_library_install_btn = PushButton('')
    window.browser_library_install_btn.setIcon(FIF.ADD)
    window.browser_library_install_btn.clicked.connect(lambda: window.switchTo(window.install_browser_page))
    header_row.addWidget(window.browser_library_install_btn)
    layout.addLayout(header_row)

    window.browser_library_card = SimpleCardWidget()
    card_layout = QtWidgets.QVBoxLayout(window.browser_library_card)
    card_layout.setContentsMargins(16, 12, 16, 16)
    card_layout.setSpacing(10)

    window.browser_library_group_title = StrongBodyLabel('')
    card_layout.addWidget(window.browser_library_group_title)
    card_layout.addWidget(HorizontalSeparator())

    window.browser_library_list = ListWidget()
    window.browser_library_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
    window.browser_library_list.customContextMenuRequested.connect(window._show_browser_library_menu)
    card_layout.addWidget(window.browser_library_list, 1)

    action_row = QtWidgets.QHBoxLayout()
    window.browser_library_refresh_btn = PushButton('')
    window.browser_library_refresh_btn.setIcon(FIF.SYNC)
    window.browser_library_refresh_btn.clicked.connect(window.refresh_browser_library)
    action_row.addWidget(window.browser_library_refresh_btn)
    action_row.addStretch(1)
    card_layout.addLayout(action_row)

    layout.addWidget(window.browser_library_card, 1)


def build_install_browser_page(window) -> None:
    window.install_browser_page = QtWidgets.QWidget()
    window.install_browser_page.setObjectName('installBrowserPage')
    layout = QtWidgets.QVBoxLayout(window.install_browser_page)
    layout.setContentsMargins(24, 24, 24, 24)
    layout.setSpacing(16)
    layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

    window.install_browser_title = TitleLabel('')
    layout.addWidget(window.install_browser_title)

    window.install_browser_subtitle = SubtitleLabel('')
    window.install_browser_subtitle.setVisible(False)
    layout.addWidget(window.install_browser_subtitle)

    window.install_browser_card = SimpleCardWidget()
    card_layout = QtWidgets.QVBoxLayout(window.install_browser_card)
    card_layout.setContentsMargins(16, 12, 16, 16)
    card_layout.setSpacing(10)

    window.install_browser_group_title = StrongBodyLabel('')
    card_layout.addWidget(window.install_browser_group_title)
    card_layout.addWidget(HorizontalSeparator())

    form_container = QtWidgets.QWidget()
    form = QtWidgets.QFormLayout(form_container)
    form.setVerticalSpacing(10)
    form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

    window.install_version_combo = ComboBox()
    window.install_label_version = QtWidgets.QLabel()
    form.addRow(window.install_label_version, window.install_version_combo)

    card_layout.addWidget(form_container)

    action_row = QtWidgets.QHBoxLayout()
    window.install_browser_btn = PrimaryPushButton('')
    window.install_browser_btn.setIcon(FIF.SYNC)
    window.install_browser_btn.clicked.connect(window._start_install_browser)
    action_row.addWidget(window.install_browser_btn)
    action_row.addStretch(1)
    card_layout.addLayout(action_row)

    window.install_progress = IndeterminateProgressBar()
    window.install_progress.setVisible(False)
    card_layout.addWidget(window.install_progress)

    layout.addWidget(window.install_browser_card)
    layout.addStretch(1)


def build_navigation(window) -> None:
    window.nav_home = window.addSubInterface(window.home_page, FIF.HOME, window._t('nav_home'))
    window.nav_launch = window.addSubInterface(window.launch_page, FIF.PLAY, window._t('nav_launch'))
    window.nav_profiles = window.addSubInterface(window.profiles_page, FIF.PEOPLE, window._t('nav_profiles'))
    window.nav_browser_library = window.addSubInterface(
        window.browser_library_page, FIF.GLOBE, window._t('nav_browser_library')
    )
    window.nav_install_browser = window.addSubInterface(
        window.install_browser_page, FIF.SYNC, window._t('nav_install_browser')
    )
    window.nav_onboarding = window.addSubInterface(
        window.onboarding_page, FIF.HELP, ''
    )
    window.nav_onboarding.setVisible(False)
    window.nav_settings = window.addSubInterface(window.settings_page, FIF.SETTING, window._t('nav_settings'))
    window.switchTo(window.home_page)
