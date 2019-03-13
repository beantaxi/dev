set copyindent
set noexpandtab
set preserveindent
set softtabstop=0
set shiftwidth=3
set tabstop=3
set autoindent
set hidden
set wildmenu
set wildmode=list:longest
set scrolloff=3
set backupdir=~/.vim-temps,~/.tmp,~/tmp,/var/tmp,/tmp
set directory=~/.vim-temps,~/.tmp,~/tmp,/var/tmp,/tmp
nnoremap <C-e> 3<C-e>
nnoremap <C-y> 3<C-y>
set ruler

augroup myCommands
	autocmd!
	autocmd InsertLeave,TextChanged * if expand('%') != '' | update | endif
	au BufRead,BufNewFile *.pyp setfiletype html
augroup END

map <C-S> <Esc>:w<CR>
map <C-Tab> <Esc>:tabnext<CR>
map <C-Left> <Esc>:tabprev<CR>
map <C-Right> <Esc>:tabnext<CR>
map <C-n> <Esc>:tabnew<CR>
map <CR> O<Esc>j
map <S-CR> d/\s*<CR>i<CR><Esc>

set sessionoptions+=resize,winpos
syntax on
