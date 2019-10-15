!sign prime number 2 to 100000000
!Fcode team
!ponychen fix a bug
!2019/10/14

program main
      integer(4) :: i,j,k,m,n,d
      integer(4),parameter :: mx=100000000,mx1=mx*1.1
      integer(1) :: a(mx1)
      real :: x1,x2
      call cpu_time(x1)
      a=0
      a(2:3)=1
      m=2
      n=sqrt(mx*1.0)

      a(6-1:mx-1:6)=1
      a(6+1:mx+1:6)=1
      do i=6,n,6
      do j=i-1,i+1,2
      if(a(j)==0) cycle
      n=j*j
      d=j*2
      do k=n,mx,d
      if(mod(k,6)==3) exit
      a(k)=0
      end do
      n=k+d
      do k=n,mx,d*3
      if(a(k)/=0) a(k)=0
      if(a(k+d)/=0) a(k+d)=0
      end do
      end do
      end do

      do i=6,mx,6
      m=m+a(i-1)+a(i+1)
      end do
      call cpu_time(x2)
      write(*,"(1x,2i8,a)") m,int((x2-x1)*1000.0),' ms '
      end program
