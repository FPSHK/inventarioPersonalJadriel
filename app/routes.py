from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import ItemForm, ChangePasswordForm  #importando de la aplicacion forms (Janiel)
from app.models import db, Item, User

#Blueprint principal que maneja el dashboard, gestion de items y cambio de contraseña 
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Pagina de inicio publica (el home)
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        #Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect', 'danger')
            return render_template('cambiar_password.html', form=form)
        
        #Actualiza contraseña y guarda 
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash(' Password updated successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario, muestra los items del inventario
    """
    if current_user.role.name == 'Admin':
        items = Item.query.all()
    else:
        items = Item.query.filter_by(owner_id=current_user.id).all()
    
    return render_template ('dashboard.html', items=items)

@main.route('/items', methods=['GET', 'POST'])
@login_required
def items():
    """
    Permite crear un nuevo item. Disponible solo para owner o admins
    """
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            nombre=form.nombre.data,
            categoria=form.categoria.data,
            cantidad=form.cantidad.data,
            precio_estimado=form.precio_estimado.data,
            ubicacion=form.ubicacion.data,
            fecha_adquisicion=form.fecha_adquisicion.data,
            owner_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash("Item created successfully.", 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('item_form.html', form=form )

@main.route('/items/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_item(id):
    """
    Permite editar un item existente. Solo si es admin o el dueño
    """
    item = Item.query.get_or_404(id)

    #validar permisos
    if current_user.role.name not in ['Admin', 'Owner'] or (
        item.owner_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to edit this item.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = ItemForm(obj=item)

    if form.validate_on_submit():
        item.nombre = form.nombre.data
        item.categoria = form.categoria.data
        item.cantidad =  form.cantidad.data
        item.precio_estimado =  form.precio_estimado.data
        item.ubicacion = form.ubicacion.data
        item.fecha_adquisicion = form.fecha_adquisicion.data
        db.session.commit()
        flash("Item updated successfully", 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('item_form.html', form=form, editar=True)

@main.route('/items/<int:id>/eliminar', methods=['POST'])
@login_required 
def eliminar_item(id):
    """
    Elimina un item si el usuario es admin o su owner creador
    """
    item = Item.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Owner'] or (
        item.owner_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to delete this item', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully", 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    """
    Lista todos los usuarios del sistema. Solo accesible para el rol Admin
    """
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page", 'danger')
        return redirect(url_for('main.dashboard'))
    
    #Obtener instancias completas de usuarios con sus roles
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)