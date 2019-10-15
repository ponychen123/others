
module rotcoordmod
      implicit none
      integer,parameter :: dp=selected_real_kind(p=9)
      contains
          subroutine rotcoord(coord,coord1,coord2,coord3)
              !matrix,point alined to origin, alined to Y, alined to XY
              !plane
              real(dp) :: coord(:,:)
              integer :: coord1,coord2,coord3
              real(dp) :: A(1,3),B(1,3),C(1,3),ab(1,3),&
                  & ac(1,3),U(3,3),Ustar(3,3)
              real(dp) :: Lab(1,1),M(3,3),I(3,3)
              !read the point alined to origin from coord to A
              A(1,:)=coord(:,coord1)
              !displace whole system so the coord1 move to origin
              coord(1,:)=coord(1,:)-A(1,1)
              coord(2,:)=coord(2,:)-A(1,2)
              coord(3,:)=coord(3,:)-A(1,3)
              !reread three point need to alin to A,B,C
              A(1,:)=coord(:,coord1)
              B(1,:)=coord(:,coord2)
              C(1,:)=coord(:,coord3)
              !a vector from A to B
              ab=B-A
              !calculate the norm of ab
              Lab=sqrt(matmul(ab,transpose(ab)))
              !calculate the anular bisector of ab 
              ab(1,:)=[ab(1,1)/2,((ab(1,2)+Lab(1,1))/2),ab(1,3)/2]
              !get the unit vector of ab
              Lab=sqrt(matmul(ab,transpose(ab)))
              ab=ab/Lab(1,1)
              
              U=matmul(transpose(ab),ab)
              !unit matrix
              I=reshape((/1.0_DP,0.0_dp,0.0_dp,0.0_dp,1.0_dp,0.0_dp,0.0_dp,&
                  & 0.0_dp,1.0_dp/),(/3,3/))
              M=2*U-I
              !rotate ABC
              A=matmul(A,transpose(M))
              B=matmul(B,transpose(M))
              C=matmul(C,transpose(M))
              coord=transpose(matmul(transpose(coord),transpose(M)))

              !rotate C to XY plane along Y
              ac=C-A
              ab(1,:)=[0.0_DP,1.0_dp,0.0_dp]
              U=matmul(transpose(ab),ab)
              !conjugate matrix of U
              Ustar=reshape((/0.0_dp,ab(1,3),-ab(1,2),-ab(1,3),0.0_dp,&
                  &ab(1,1),ab(1,2),-ab(1,1),0.0_dp/),(/3,3/))
              M=U+(I-U)*ac(1,1)/sqrt(ac(1,1)*ac(1,1)+ac(1,3)*ac(1,3))+&
                  &Ustar*ac(1,3)/sqrt(ac(1,1)*ac(1,1)+ac(1,3)*ac(1,3))
              coord=transpose(matmul(transpose(coord),transpose(M)))
              end subroutine
              end module

program main
    use rotcoordmod
    implicit none
    integer :: i,j,k,io,coordmax=0
    real(dp),allocatable :: coord(:,:)
    character(80) :: c
    open(10,file='old-coordinate.txt',status="old")
    do
    read(10,'(A)',iostat=io) c
    if (io<0)exit
    if(len_trim(c)==0)cycle
    coordmax = coordmax+1
    end do
    rewind(10)
    allocate(coord(3,coordmax))
    read(10,*) coord(:,:)
    write(*,*) "Input the Coordinate sequence, such as 2 1 3"
    read(*,*) i,j,k
    call rotcoord(coord,i,j,k)
    write(*,"(3f15.9)") coord(:,:)
    end program


