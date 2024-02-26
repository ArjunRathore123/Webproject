from .serilaizers import ProductSerializer,CartSerailizer,OrderSerializer
from rest_framework.views import APIView
from accounts.models import CustomUser
from products.models import Product,Category,Brand,Color,CartItem,Order,Wallet,SellerWallet,AdminWallet
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

import razorpay
from django.conf import settings

class ProductView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self, request, *args, **kwargs):
        product=Product.objects.all()
        print(product)
        serializer=ProductSerializer(product,many=True)
        context={
            'success':True,
            'status':status.HTTP_200_OK,
            'data':serializer.data
        }
        return Response(context)
     
    def post(self, request, *args, **kwargs):
      
        try:
            print(request.data,"=====1")
            category_id=request.query_params.get('category_id')
            brand_id = request.query_params.get('brand_id')
            print(category_id,"==",brand_id)
            if request.user.user_type == 'seller':
                category = Category.objects.get(id=category_id)
                brand = Brand.objects.get(id=brand_id)
                data = request.data
                print(data)
                print("======================1")
                name = data["product_name"]
                descr= data["description"]
                price = data["price"]
                quant = data["quantity"]
                img = data["product_image"]
              
                colors_data = data.pop('color', [])
                a=colors_data[0].split(',')
                print(a)

                product = Product.objects.create(
                    category = category,
                    brand = brand,
                    price =  price,
                    description = descr,
                    product_name = name,
                    quantity = quant,
                    product_image = img,
                    user_id = request.user.id
                   
                )
                for colors_data in a:
                    color, created = Color.objects.get_or_create(color=colors_data)
                    product.color.add(color)
                print(product,colors_data)
                print("======================2")
                
                context = {
                    'success': True,
                    'status': status.HTTP_201_CREATED,
                    'msg':'Product created successfully',
                    'data': ProductSerializer(product).data
                }

                return Response(context)

            return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': 'Unauthorized User'
            })
        except Category.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': 'Category not found'
            })

        except Brand.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': 'Brand not found'
            })

        except Color.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': 'One or more colors not found'
            })

        except Exception as e:
            return Response({
                'success': False,
                'data': str(e)
            })

    def put(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        brand_id = request.query_params.get('brand_id')
        category_id=request.query_params.get('category_id')
        if request.user.user_type=='seller':
            product=Product.objects.get(id=product_id)
            category = Category.objects.get(id=category_id)
            brand = Brand.objects.get(id=brand_id)
            data = request.data
            print(data)
            print("======================1")
            name = data["product_name"]
            descr= data["description"]
            price = data["price"]
            quant = data["quantity"]
            img = data["product_image"]
            
            colors_data = data.pop('color', [])
            a=colors_data[0].split(',')
            print(a)

            
            product.category = category
            product.brand = brand
            product.price = price
            product.description = descr
            product.product_name = name
            product.quantity = quant
            product.product_image = img
            product.save()

            for colors_data in a:
                color,created = Color.objects.get_or_create(color=colors_data)
                product.color.add(color)
            print(product,colors_data)
            context={
                'success':True,
                'status':status.HTTP_205_RESET_CONTENT,
                'msg':'Product update successfully',
                'data':ProductSerializer(product).data
            }
            return Response(context)
           
        return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': 'Unauthorized User'
            })
           
    def delete(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        if request.user.user_type=='seller':
           product=Product.objects.get(id=product_id)
           product.delete()
           context={
                   'success':True,
                   'status':status.HTTP_204_NO_CONTENT,
                   'msg':'Product deleted successfully',
                   'data':{}
               }
           return Response(context)
        return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': 'Unauthorized User'
            }) 

class SellerProductView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self, request, *args, **kwargs):
        user_id=request.query_params.get('user_id')
        if request.user.user_type == 'seller':
            user=CustomUser.objects.get(id=user_id)
            product=Product.objects.filter(user=user)
            serializer=ProductSerializer(product,many=True)
            context={
            'success':True,
            'status':status.HTTP_200_OK,
            'data':serializer.data
            }
            return Response(context)
        return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': 'Unauthorized User'
            })
    

class AddtoCartView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        if request.user.user_type=='buyer':
            try:
               product=Product.objects.get(id=product_id)
            except Product.DoesNotExist:
               return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            cart_item,created=CartItem.objects.get_or_create(user=request.user,product=product)
            product.quantity-=1
            product.save()
            if not created:
                cart_item.quantity+=1
                cart_item.save()
            
            serializer=CartSerailizer(cart_item)
            context={
                'success':True,
                'status':status.HTTP_201_CREATED,
                'data':serializer.data
            }
            return Response(context)
        return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': 'Unauthorized User'
            })
    
class RemoveCartView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def delete(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        if request.user.user_type=='buyer':
            try:
                product=Product.objects.get(id=product_id)
                cartitem=CartItem.objects.get(product=product,user=request.user)
            except CartItem.DoesNotExist:
                return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
            if cartitem.quantity>=1:
                if cartitem.quantity is not None:
                    product.quantity=product.quantity+cartitem.quantity
                    product.save()
                    cartitem.delete()
                    context={
                    'success':True,
                    'status':status.HTTP_204_NO_CONTENT,
                    'data':'Item remove successfully'
                    }
                    return Response(context)
                    
               
class IncreaseCartItemView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args,**kwargs):
        product_id=request.query_params.get('product_id')
        if request.user.user_type=='buyer':
            product=Product.objects.get(id=product_id)
            cartitem=CartItem.objects.get(product=product,user=request.user)
            cartitem.quantity+=1
            product.quantity-=1
            cartitem.save()
            product.save()
            serializer=CartSerailizer(cartitem)
            context={
                'success':True,
                'status':status.HTTP_200_OK,
                'data':serializer.data
            }
            return Response(context)
        return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': 'Unauthorized User'
            })
        

class DecreaseCartItemView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args,**kwargs):
        product_id=request.query_params.get('product_id')
        
        if request.user.user_type=='buyer':
            product=Product.objects.get(id=product_id)
            cartitem=CartItem.objects.get(product=product,user=request.user)
            if cartitem.quantity>1:
                cartitem.quantity-=1
                product.quantity+=1
                cartitem.save()
                product.save()
                serializer=CartSerailizer(cartitem)
                context={
                    'success':True,
                    'status':status.HTTP_200_OK,
                    'data':serializer.data
                }
                return Response(context)
            else:
                cartitem.delete()
                context={
                    'success':True,
                    'status':status.HTTP_204_NO_CONTENT,
                    'data':serializer.data
                }
                return Response(context)

        return Response({
                'success': False,
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': 'Unauthorized User'
            })
        

class CreateOrderView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        user=CustomUser.objects.get(id=request.user.id)
        cartitem=CartItem.objects.filter(user=request.user)
        product=Product.objects.get(id=product_id)

        if not cartitem.exists():
            return Response({'msg':'Cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        city=request.data.get('city')
        pincode=request.data.get('pincode')
        order_data={
            'user':user.id,
            'product':product.id,
            'city':city,
            'pincode':pincode,
        }

        serializer=OrderSerializer(data=order_data)
        if serializer.is_valid():
            order=serializer.save()
            price=sum(item.subtotal() for item in cartitem)

            client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
            payment=client.order.create({'amount': price*100, "currency": "INR", 'payment_capture': 1})
            print(payment)
            order.razorpay_order_id=payment['id']
            
            cartitem.delete()
            order.save()
            context = {'success':True,
                'status':status.HTTP_201_CREATED,
                'payment': payment, 'total_price': price}
            return Response(context)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderCancelView(APIView):
    def delete(self,request,*args,**kwargs):
        order_id=request.query_params.get('order_id')
        try:
            order=Order.objects.get(razorpay_order_id=order_id)
            order.delete()
            return Response({'message': f'Order {order_id} cancelled successfully.'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': f'Order {order_id} not found.'}, status=status.HTTP_404_NOT_FOUND)


class PaymentSuccessView(APIView):
    def put(self, request,*args, **kwargs):
        order_id=request.query_params.get('order_id')
        try:
            user = CustomUser.objects.get(id=request.user.id)
            order = Order.objects.get(razorpay_order_id=order_id)
            admin_user=CustomUser.objects.get(email='admin@gmail.com')
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or does not belong to the user'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data=request.data
       
        total_amount=int(request.data.get('total_price'))
        print(total_amount)
      

        if order.is_paid:
            return Response({'error': 'Order is already paid'}, status=status.HTTP_400_BAD_REQUEST)
        buyerwallet=Wallet.objects.get(user=user)
        if buyerwallet.balance>=total_amount:
            
            buyerwallet.balance-=total_amount
            buyerwallet.save()

            adminwallet,created=AdminWallet.objects.get_or_create(user=admin_user)
            admin_commission=(total_amount*5)/100
            adminwallet.balance+=admin_commission
            adminwallet.save()

            sellerwallet,created=SellerWallet.objects.get_or_create(user=order.product.user)
            sellerwallet.balance+=total_amount-admin_commission
            sellerwallet.save()

            order.is_paid=True
            order.save()

            serializer = OrderSerializer(order)
        else:
            order.is_paid=False
            order.save()
            return Response({'error':'Insufficent Balance'},status=status.HTTP_400_BAD_REQUEST)    

        return Response(serializer.data, status=status.HTTP_200_OK)




