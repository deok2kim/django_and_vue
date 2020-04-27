# README

1. 로그인

   ```python
   def login(request):
       if request.method == 'POST':
           form = AuthenticationForm(request, request.POST)
           if form.is_valid():
               auth_login(request, form.get_user())
               return redirect('accounts:index')
       else:
           form = AuthenticationForm()
       context = {
           'form': form,
       }
       return render(request, 'accounts/login.html',context)
   ```

   ```python
   auth_login(request, form.get_user())
   ```

   

2. 이미 인증되어있는 사용자

   ```python
   if request.user.is_authenticated:
       return redirect('community:review_list')
   # 생각보다 쉽게 끝났다
   ```

   

3. 로그인 시 기존 URL이 함께 넘어왔다면 해당 URL로 

   ```python
   return redirect(request.GET.get('next') or 'community:review_list')
   ```

   