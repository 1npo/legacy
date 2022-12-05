" vim-plug
"
call plug#begin('~/.config/nvim/plugged')
Plug 'https://github.com/jceb/vim-orgmode.git'
Plug 'https://github.com/drewtempelmeyer/palenight.vim'
Plug 'https://github.com/ayu-theme/ayu-vim.git'
call plug#end()

" theme
"
colorscheme ayu
let ayucolor="mirage"
set termguicolors


let g:palenight_terminal_italics=1

" syntax coloring
"
syntax on

" enable mouse support
"
set mouse=a

" sane tabs
"
set tabstop=4
set softtabstop=0 noexpandtab
set shiftwidth=4

" put viminfo in ~/.vim instead of ~
"
set viminfo+=n~/.vim/viminfo

" use sane indentation when wrapping long lines in lists
"
set linebreak
set wrap
set nolist
set breakindent
let &showbreak='  '

