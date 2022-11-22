import Vue from 'vue'
import {
  Form,
  FormItem,
  Input,
  Button,
  Message,
  MessageBox,
  Container,
  Aside,
  Main,
  Header,
  Menu,
  Submenu,
  MenuItem,
  Card,
  Breadcrumb,
  BreadcrumbItem,
  Row, Col,
  Table, TableColumn,
  Dialog,
  Pagination,
  Switch,
  Tooltip,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Tree, Select, Option, DatePicker,
  Upload
} from 'element-ui' // 按需导入Ele UI

Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Button)
Vue.use(Container)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Header)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Card)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Dialog)
Vue.use(Pagination)
Vue.use(Switch)
Vue.use(Tooltip)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.use(Tree)
Vue.use(Select)
Vue.use(Option)
Vue.use(DatePicker)
Vue.use(Upload)

// 全局导入
Vue.prototype.$message = Message
Vue.prototype.$messageBox = MessageBox
Vue.prototype.$confirm = MessageBox.confirm